#ifndef OpenKAI_src_Autopilot_AP__AProver_drive_H_
#define OpenKAI_src_Autopilot_AP__AProver_drive_H_

#include "_AP_base.h"
#include "../../../Control/_Drive.h"

namespace kai
{

class _AProver_drive: public _StateBase
{
public:
	_AProver_drive();
	~_AProver_drive();

	virtual	bool init(void* pKiss);
	virtual bool start(void);
	virtual int check(void);
	virtual void update(void);
	virtual void draw(void);

	virtual void setYawMode(bool bRelative);

protected:
	bool updateDrive(void);
	static void* getUpdate(void* This)
	{
		((_AProver_drive *) This)->update();
		return NULL;
	}

public:
	_AP_base* 	m_pAP;
    _Drive*      m_pD;

	bool	m_bSetYawSpeed;
    float   m_yawMode;
	bool	m_bRcChanOverride;
	float	m_pwmM;
	float	m_pwmD;
	uint16_t* m_pRcYaw;
	uint16_t* m_pRcThrottle;
	mavlink_rc_channels_override_t m_rcOverride;

};

}
#endif
