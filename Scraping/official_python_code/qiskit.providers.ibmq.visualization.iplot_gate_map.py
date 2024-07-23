#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit.test.ibmq_mock import mock_get_backend
mock_get_backend('FakeVigo')


# In[2]:


from qiskit import IBMQ
from qiskit.providers.ibmq.visualization import iplot_gate_map

IBMQ.load_account()

provider = IBMQ.get_provider(group='open', project='main')
backend = provider.get_backend('ibmq_vigo')

iplot_gate_map(backend, as_widget=True)

