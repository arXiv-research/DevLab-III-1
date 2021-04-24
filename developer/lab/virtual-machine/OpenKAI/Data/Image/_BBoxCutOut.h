/*
 * _BBoxCutOut.h
 *
 *  Created on: Sept 16, 2017
 *      Author: yankai
 */

#ifndef OpenKAI_src_Data_Image__BBoxCutOut_H_
#define OpenKAI_src_Data_Image__BBoxCutOut_H_

#include "../../Base/_ModuleBase.h"

#ifdef USE_OPENCV

namespace kai
{

class _BBoxCutOut: public _ModuleBase
{
public:
	_BBoxCutOut();
	~_BBoxCutOut();

	bool init(void* pKiss);
	bool start(void);

private:
	void process();
	void update(void);
	static void* getUpdate(void* This)
	{
		((_BBoxCutOut*) This)->update();
		return NULL;
	}

public:
	string m_dirIn;
	string m_dirOut;
	string m_extTxt;
	string m_extImgIn;
	string m_extImgOut;

};

}
#endif
#endif
