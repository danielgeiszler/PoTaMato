# -*- coding: utf-8 -*-

import statsmodels.api as sm
import statsmodels.formula.api as smf

data = sm.datasets.get_rdataset("dietox", "geepack").data

print(data)