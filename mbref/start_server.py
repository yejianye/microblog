#!/usr/bin/env python
from mbref.app import app

# Register APIs
import mbref.www.api

app.debug = True
app.run(port=7431)
