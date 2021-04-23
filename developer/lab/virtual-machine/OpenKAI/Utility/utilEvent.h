#ifndef OpenKAI_src_Utility_utilEvent_H_
#define OpenKAI_src_Utility_utilEvent_H_

namespace kai
{

struct INTERVAL_EVENT
{
	uint64_t m_tLastEvent;
	uint64_t m_tInterval;

	void init(uint64_t uInt)
	{
		m_tInterval = uInt;
		reset();
	}

	bool update(uint64_t tNow)
	{
		IF_F(tNow - m_tLastEvent < m_tInterval);

		m_tLastEvent = tNow;
		return true;
	}

	void reset(void)
	{
		m_tLastEvent = 0;
	}
};

struct STATE_CHANGE
{
	int m_state;
	bool m_bChanged;

	void init(int state)
	{
		m_state = state;
		m_bChanged = false;
	}

	void update(int state)
	{
		IF_(m_state == state);

		m_bChanged = true;
		m_state = state;
	}

	bool bActive(int state)
	{
		IF_F(m_state != state);
		IF_F(!m_bChanged);

		m_bChanged = false;
		return true;
	}
};

}
#endif
