/*
 * _RealSense.cpp
 *
 *  Created on: Apr 6, 2018
 *      Author: yankai
 */

#include "_RealSense.h"

#ifdef USE_OPENCV
#ifdef USE_REALSENSE

namespace kai
{

_RealSense::_RealSense()
{
    m_type = vision_realsense;
    m_pTPP = NULL;

    m_rsSN = "";
    m_vPreset = "High Density";
    m_bRsRGB = true;
    m_rsFPS = 30;
    m_rsDFPS = 30;
    m_fDec = 0.0;
    m_fSpat = 0.0;
    m_bAlign = false;
    m_rspAlign = NULL;
    m_fEmitter = 1.0;
    m_fLaserPower = 1.0;
    m_iHistFrom = 0;
}

_RealSense::~_RealSense()
{
    DEL ( m_pTPP );
    DEL ( m_rspAlign );
}

bool _RealSense::init ( void* pKiss )
{
    IF_F ( !_DepthVisionBase::init ( pKiss ) );
    Kiss* pK = ( Kiss* ) pKiss;

    pK->v ( "rsSN", &m_rsSN );
    pK->v ( "rsFPS", &m_rsFPS );
    pK->v ( "rsDFPS", &m_rsDFPS );
    pK->v ( "vPreset", &m_vPreset );
    pK->v ( "bRsRGB", &m_bRsRGB );
    pK->v ( "fDec", &m_fDec );
    pK->v ( "fSpat", &m_fSpat );
    pK->v ( "bAlign", &m_bAlign );
    pK->v ( "fEmitter", &m_fEmitter );
    pK->v ( "fLaserPower", &m_fLaserPower );
    
    Kiss* pKt = pK->child("threadPP");
    IF_F(pKt->empty());
    
    m_pTPP = new _Thread();
    if(!m_pTPP->init(pKt))
    {
        DEL(m_pTPP);
        return false;
    }

    return true;
}

bool _RealSense::open ( void )
{
    IF_T ( m_bOpen );

    try
    {
        if ( !m_rsSN.empty() )
            m_rsConfig.enable_device ( m_rsSN );

        m_rsConfig.enable_stream ( RS2_STREAM_DEPTH, m_vDsize.x, m_vDsize.y, RS2_FORMAT_Z16, m_rsDFPS );
        if ( m_bRsRGB )
            m_rsConfig.enable_stream ( RS2_STREAM_COLOR, m_vSize.x, m_vSize.y, RS2_FORMAT_BGR8, m_rsFPS );

        m_rsProfile = m_rsPipe.start(m_rsConfig);
        rs2::device dev = m_rsProfile.get_device();
        LOG_I("Device Name:" + string(dev.get_info(RS2_CAMERA_INFO_NAME)));
        LOG_I("Firmware Version:" + string(dev.get_info(RS2_CAMERA_INFO_FIRMWARE_VERSION)));
        LOG_I("Serial Number:" + string(dev.get_info(RS2_CAMERA_INFO_SERIAL_NUMBER)));
        LOG_I("Product Id:" + string(dev.get_info(RS2_CAMERA_INFO_PRODUCT_ID)));
        
        auto cStream = m_rsProfile.get_stream ( RS2_STREAM_COLOR ).as<rs2::video_stream_profile>();
        m_cIntrinsics = cStream.get_intrinsics();
        auto dStream = m_rsProfile.get_stream ( RS2_STREAM_DEPTH ).as<rs2::video_stream_profile>();
        m_dIntrinsics = dStream.get_intrinsics();

        auto sensor = m_rsProfile.get_device().first<rs2::depth_sensor>();
        m_dScale = sensor.get_depth_scale();

        auto range = sensor.get_option_range ( RS2_OPTION_VISUAL_PRESET );
        for ( auto i = range.min; i <= range.max; i += range.step )
        {
            string preset = std::string ( sensor.get_option_value_description ( RS2_OPTION_VISUAL_PRESET, i ) );
            IF_CONT ( preset != m_vPreset );
            sensor.set_option ( RS2_OPTION_VISUAL_PRESET, i );
            break;
        }

        if ( m_fDec > 0.0 )
            m_rsfDec.set_option ( RS2_OPTION_FILTER_MAGNITUDE, m_fDec );
        if ( m_fSpat > 0.0 )
            m_rsfSpat.set_option ( RS2_OPTION_HOLES_FILL, m_fSpat );

        if ( sensor.supports ( RS2_OPTION_EMITTER_ENABLED ) )
            sensor.set_option ( RS2_OPTION_EMITTER_ENABLED, m_fEmitter );

        if ( sensor.supports ( RS2_OPTION_LASER_POWER ) )
        {
            auto range = sensor.get_option_range ( RS2_OPTION_LASER_POWER );
            sensor.set_option ( RS2_OPTION_LASER_POWER, range.max * m_fLaserPower );
        }

        rs2::frameset rsFrameset = m_rsPipe.wait_for_frames();

        if ( m_bRsRGB )
        {
            if ( m_bAlign )
            {
                m_rspAlign = new rs2::align ( rs2_stream::RS2_STREAM_COLOR );
                rs2::frameset rsFramesetAlign = m_rspAlign->process ( rsFrameset );
                m_rsColor = rsFramesetAlign.get_color_frame();
                m_rsDepth = rsFramesetAlign.get_depth_frame();
            }
            else
            {
                m_rsColor = rsFrameset.get_color_frame();
                m_rsDepth = rsFrameset.get_depth_frame();
            }

            m_vSize.x = m_rsColor.as<rs2::video_frame>().get_width();
            m_vSize.y = m_rsColor.as<rs2::video_frame>().get_height();
        }
        else
        {
            m_rsDepth = rsFrameset.get_depth_frame();
        }

        if ( m_fDec > 0.0 )
            m_rsDepth = m_rsfDec.process ( m_rsDepth );
        if ( m_fSpat > 0.0 )
            m_rsDepth = m_rsfSpat.process ( m_rsDepth );

        m_vDsize.x = m_rsDepth.as<rs2::video_frame>().get_width();
        m_vDsize.y = m_rsDepth.as<rs2::video_frame>().get_height();

    }
    catch ( const rs2::camera_disconnected_error& e )
    {
        LOG_E ( "Realsense disconnected" );
        return false;
    }
    catch ( const rs2::recoverable_error& e )
    {
        LOG_E ( "Realsense open failed" );
        return false;
    }
    catch ( const rs2::error& e )
    {
        LOG_E ( "Realsense error" );
        return false;
    }
    catch ( const std::exception& e )
    {
        LOG_E ( "Realsense exception" );
        return false;
    }

    m_bOpen = true;
    return true;
}

void _RealSense::hardwareReset ( void )
{
//    m_rsConfig.resolve(m_rsPipe).get_device().hardware_reset();
    rs2::device dev = m_rsProfile.get_device();
    dev.hardware_reset();
}

void _RealSense::close ( void )
{
    this->_VisionBase::close();
    m_rsPipe.stop();
}

bool _RealSense::start ( void )
{
    NULL_F(m_pT);
    NULL_F(m_pTPP);
    IF_F(!m_pT->start(getUpdate, this));
	return m_pTPP->start(getUpdate, this);
}

int _RealSense::check(void)
{
    NULL__(m_pT, -1);
    NULL__(m_pTPP, -1);
    
	return _DepthVisionBase::check();
}

void _RealSense::update ( void )
{
    while(m_pT->bRun())
    {
        if ( !m_bOpen )
        {
            if ( !open() )
            {
                LOG_E ( "Cannot open RealSense" );
                hardwareReset();
                m_pT->sleepT ( SEC_2_USEC );
                continue;
            }
        }

        m_pT->autoFPSfrom();

        if ( updateRS() )
        {
            m_pTPP->wakeUp();
        }
        else
        {
            hardwareReset();
            m_pT->sleepT ( SEC_2_USEC );
            m_bOpen = false;
        }

        m_pT->autoFPSto();
    }
}

bool _RealSense::updateRS ( void )
{
    IF_T ( check() < 0 );

    try
    {
        rs2::frameset rsFrameset = m_rsPipe.wait_for_frames();

        if ( m_bRsRGB )
        {
            if ( m_bAlign )
            {
                rs2::frameset rsFramesetAlign = m_rspAlign->process ( rsFrameset );
                m_rsColor = rsFramesetAlign.get_color_frame();
                m_rsDepth = rsFramesetAlign.get_depth_frame();
            }
            else
            {
                m_rsColor = rsFrameset.get_color_frame();
                m_rsDepth = rsFrameset.get_depth_frame();
            }

            m_fBGR.copy ( Mat ( Size ( m_vSize.x, m_vSize.y ), CV_8UC3, ( void* ) m_rsColor.get_data(), Mat::AUTO_STEP ) );
        }
        else
        {
            m_rsDepth = rsFrameset.get_depth_frame();
        }

    }
    catch ( const rs2::camera_disconnected_error& e )
    {
        LOG_E ( "Realsense disconnected" );
        return false;
    }
    catch ( const rs2::recoverable_error& e )
    {
        LOG_E ( "Realsense open failed" );
        return false;
    }
    catch ( const rs2::error& e )
    {
        LOG_E ( "Realsense error" );
        return false;
    }
    catch ( const std::exception& e )
    {
        LOG_E ( "Realsense exception" );
        return false;
    }

    return true;
}

void _RealSense::updateTPP ( void )
{
    while(m_pTPP->bRun())
    {
        m_pTPP->sleepT ( 0 );

        if ( m_fDec > 0.0 )
            m_rsDepth = m_rsfDec.process ( m_rsDepth );
        if ( m_fSpat > 0.0 )
            m_rsDepth = m_rsfSpat.process ( m_rsDepth );
        if ( m_pDepthWin )
            m_rsDepthShow = m_rsDepth;

        Mat mZ = Mat ( Size ( m_vDsize.x, m_vDsize.y ), CV_16UC1, ( void* ) m_rsDepth.get_data(), Mat::AUTO_STEP );
        Mat mD;
        mZ.convertTo ( mD, CV_32FC1 );

        m_fDepth = mD * m_dScale;
    }
}

void _RealSense::draw ( void )
{
    if ( m_pDepthWin )
    {
        IF_ ( m_fDepth.bEmpty() );
        rs2::colorizer rsColorMap;
        rs2::frame dColor = rsColorMap.process ( m_rsDepthShow );
        Mat mDColor ( Size ( m_vDsize.x, m_vDsize.y ), CV_8UC3, ( void* ) dColor.get_data(),
                      Mat::AUTO_STEP );
        m_depthShow = mDColor;
    }

    this->_DepthVisionBase::draw();
}

}
#endif
#endif
