#include "_AProver_drive.h"

namespace kai
{

_AProver_drive::_AProver_drive()
{
	m_pAP = NULL;
    m_pD = NULL;

	m_yawMode = 1.0;
	m_bSetYawSpeed = false;
	m_bRcChanOverride = false;
	m_pwmM = 1500;
	m_pwmD = 500;
	m_pRcYaw = NULL;
	m_pRcThrottle = NULL;
}

_AProver_drive::~_AProver_drive()
{
}

bool _AProver_drive::init(void* pKiss)
{
	IF_F(!this->_StateBase::init(pKiss));
	Kiss* pK = (Kiss*) pKiss;

	pK->v("bSetYawSpeed",&m_bSetYawSpeed);
	pK->v("yawMode",&m_yawMode);
	pK->v("bRcChanOverride",&m_bRcChanOverride);

	uint16_t* pRC[19];
	pRC[0] = NULL;
	pRC[1] = &m_rcOverride.chan1_raw;
	pRC[2] = &m_rcOverride.chan2_raw;
	pRC[3] = &m_rcOverride.chan3_raw;
	pRC[4] = &m_rcOverride.chan4_raw;
	pRC[5] = &m_rcOverride.chan5_raw;
	pRC[6] = &m_rcOverride.chan6_raw;
	pRC[7] = &m_rcOverride.chan7_raw;
	pRC[8] = &m_rcOverride.chan8_raw;
	pRC[9] = &m_rcOverride.chan9_raw;
	pRC[10] = &m_rcOverride.chan10_raw;
	pRC[11] = &m_rcOverride.chan11_raw;
	pRC[12] = &m_rcOverride.chan12_raw;
	pRC[13] = &m_rcOverride.chan13_raw;
	pRC[14] = &m_rcOverride.chan14_raw;
	pRC[15] = &m_rcOverride.chan15_raw;
	pRC[16] = &m_rcOverride.chan16_raw;
	pRC[17] = &m_rcOverride.chan17_raw;
	pRC[18] = &m_rcOverride.chan18_raw;
    
    for(int i=1; i<19; i++)
        *pRC[i] = UINT16_MAX;

	int iRcYaw = 1;
	pK->v("iRcYaw", &iRcYaw);
	IF_Fl(iRcYaw <=0 || iRcYaw > 18, "RC yaw channel exceeds limit");
	m_pRcYaw = pRC[iRcYaw];
    
	int iRcThrottle = 3;
	pK->v("iRcThrottle", &iRcThrottle);
	IF_Fl(iRcThrottle <=0 || iRcThrottle > 18, "RC throttle channel exceeds limit");
	m_pRcThrottle = pRC[iRcThrottle];

	pK->v("pwmM", &m_pwmM);
	pK->v("pwmD", &m_pwmD);

	string n;
    
	n = "";
	pK->v("_AP_base", &n );
	m_pAP = (_AP_base*) (pK->getInst( n ));
	IF_Fl(!m_pAP, n + ": not found");

	n = "";
	pK->v("_Drive", &n );
	m_pD = ( _Drive*) (pK->getInst( n ));
	IF_Fl(!m_pD, n + ": not found");

    return true;
}

bool _AProver_drive::start(void)
{
    NULL_F(m_pT);
	return m_pT->start(getUpdate, this);
}

int _AProver_drive::check(void)
{
	NULL__(m_pAP,-1);
	NULL__(m_pAP->m_pMav,-1);
    NULL__(m_pD, -1);

	return this->_StateBase::check();
}

void _AProver_drive::update(void)
{
	while(m_pT->bRun())
	{
		m_pT->autoFPSfrom();

		updateDrive();

		m_pT->autoFPSto();
	}
}

bool _AProver_drive::updateDrive(void)
{
	IF_F(check() < 0);
	if(!bActive())
    {
     	IF_F(!m_bRcChanOverride);
		*m_pRcYaw = 0;
		*m_pRcThrottle = 0;
		m_pAP->m_pMav->rcChannelsOverride(m_rcOverride);
        return false;
    }
    
    float nSpd = m_pD->getSpeed() * m_pD->getDirection();
    float nStr = m_pD->getSteering();
    
	if(m_bSetYawSpeed)
	{
		m_pAP->m_pMav->clNavSetYawSpeed( nStr,
										  nSpd,
										m_yawMode);
	}

	if(m_bRcChanOverride)
	{
		*m_pRcYaw = constrain( nStr * m_pwmD + m_pwmM,
                              m_pwmM - m_pwmD,
                              m_pwmM + m_pwmD);
		*m_pRcThrottle = constrain( nSpd * m_pwmD + m_pwmM,
                                   m_pwmM - m_pwmD,
                                   m_pwmM + m_pwmD);
		m_pAP->m_pMav->rcChannelsOverride(m_rcOverride);
	}

	return true;
}

void _AProver_drive::setYawMode(bool bRelative)
{
	if(bRelative)
		m_yawMode = 1.0;
	else
		m_yawMode = 0.0;
}

void _AProver_drive::draw(void)
{
	this->_StateBase::draw();
    drawActive();
    
    NULL_(m_pRcYaw);
    NULL_(m_pRcThrottle);

	addMsg("yawMode=" + f2str(m_yawMode) + ", yaw=" + i2str(*m_pRcYaw) + ", throttle=" + i2str(*m_pRcThrottle));
}

}
