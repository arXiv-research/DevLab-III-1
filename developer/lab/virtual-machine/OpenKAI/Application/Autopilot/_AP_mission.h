#ifndef OpenKAI_src_Autopilot_AP__AP_mission_H_
#define OpenKAI_src_Autopilot_AP__AP_mission_H_

#include "../../../Base/common.h"
#include "../ArduPilot/_AP_base.h"
#include "../ArduPilot/_AP_land.h"

namespace kai
{

class _AP_mission: public _StateBase
{
public:
	_AP_mission();
	~_AP_mission();

	bool init(void* pKiss);
	bool start(void);
	int check(void);
	void update(void);
	void draw(void);

private:
	void updateMission(void);
	static void* getUpdate(void* This)
	{
		((_AP_mission*) This)->update();
		return NULL;
	}

public:
	_AP_base* m_pAP;
//	_AP_descent* m_pAPdescent;

};

}
#endif
