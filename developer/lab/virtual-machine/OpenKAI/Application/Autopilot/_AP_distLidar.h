#ifndef OpenKAI_src_Autopilot_AP__AP_distLidar_H_
#define OpenKAI_src_Autopilot_AP__AP_distLidar_H_

#include "../../../Base/common.h"
#include "../../../Sensor/_DistSensorBase.h"
#include "../ArduPilot/_AP_base.h"

#define N_LIDAR_SECTION 10

namespace kai
{

struct DIST_LIDAR_SECTION
{
	uint8_t m_orientation;
	double m_degFrom;
	double m_degTo;
	double m_minD;
	double m_sensorScale;

	void init(void)
	{
		m_orientation = 0;
		m_degFrom = 360 - 22.5;
		m_degTo = 360 + 22.5;
		m_minD = 0.0;
		m_sensorScale = 1.0;
	}
};

class _AP_distLidar: public _StateBase
{
public:
	_AP_distLidar();
	~_AP_distLidar();

	bool init(void* pKiss);
	void update(void);
	void draw(void);

private:
	void updateMavlink(void);

	_AP_base* m_pAP;
	_DistSensorBase* m_pDS;

	int	m_nSection;
	DIST_LIDAR_SECTION m_pSection[N_LIDAR_SECTION];
};

}
#endif
