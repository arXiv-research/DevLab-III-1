/*
 * _HiphenIMG.h
 *
 *  	Created on: Feb 23, 2019
 *      Author: yankai
 */

#ifndef OpenKAI_src_IO__HiphenIMG_H_
#define OpenKAI_src_IO__HiphenIMG_H_

#include "../../Base/common.h"
#include "../../IO/_TCPclient.h"
#include "../../Navigation/_GPS.h"

namespace kai
{

#define N_HIPHEN_BUF 3000000
#define N_HIPHEN_HEADER 136
#define N_HIPHEN_FILESIZE 8
#define N_HIPHEN_FILENAME 128

class _HiphenIMG: public _TCPclient
{
public:
	_HiphenIMG();
	virtual ~_HiphenIMG();

	bool init(void* pKiss);
	bool start(void);
	void decodeData(void);
	void decodeHeader(void);

	void update(void);
	static void* getUpdate(void* This)
	{
		((_HiphenIMG*) This)->update();
		return NULL;
	}

public:
	_GPS* m_pGPS;

	uint8_t m_pBuf[N_HIPHEN_BUF];
	int m_iB;
	int m_nB;
	int m_nbImg;

	string m_fileName;
	string m_dir;
};

}
#endif
