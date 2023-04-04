import os, sys
import re
import random
from pathlib import Path
import json


log_file = Path('MsaServer/log-mmseqs-msa-server.log')

get_ticket_words = 'GET /ticket/'
has_get_ticket_words = False
lines = []
for line in log_file.read_text().splitlines():
    if get_ticket_words in line:
        if has_get_ticket_words:
            continue
        else:
            lines.append(line)
        has_get_ticket_words = True
    else:
        has_get_ticket_words = False
        lines.append(line)

log_file.write_text('\n'.join(lines))