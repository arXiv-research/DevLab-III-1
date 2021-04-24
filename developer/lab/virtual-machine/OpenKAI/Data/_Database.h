/*
 * _DataBase.h
 *
 *  Created on: Oct 16, 2017
 *      Author: yankai
 */

#ifndef OpenKAI_src_Data__DataBase_H_
#define OpenKAI_src_Data__DataBase_H_

#include "../Base/_ModuleBase.h"

#ifdef USE_OPENCV
#include "../Base/cv.h"

#define D_TYPE_FILE 0x8
#define D_TYPE_FOLDER 0x4

namespace kai
{

class _DataBase: public _ModuleBase
{
public:
	_DataBase();
	~_DataBase();

	bool init(void* pKiss);
	bool start(void);

	int getDirFileList(void);
	string getExtension(string& fName);
	bool verifyExtension(string& fName);
	void setFileList(vector<string> vFileIn);

private:
	void getDirFileList(string* pStrDir);
	void update(void);
	static void* getUpdate(void* This)
	{
		((_DataBase*) This)->update();
		return NULL;
	}

public:
	string m_dirIn;
	vector<string> m_vExtIn;
	string m_extOut;

	vector<string> m_vFileIn;
	vector<int> m_vCompress;
	int m_compression;

};
}
#endif
#endif
