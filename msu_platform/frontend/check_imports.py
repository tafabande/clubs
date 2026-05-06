import os
import re

hooks = [
    'useState', 'useEffect', 'useRef', 'useCallback', 'useMemo', 
    'useContext', 'useReducer', 'useLayoutEffect',
    'useNavigate', 'useLocation', 'useParams', 'useSearchParams',
    'useQuery', 'useMutation', 'useQueryClient'
]

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for hook in hooks:
        # Check if hook is used (e.g. useState( or useState<)
        if re.search(r'\b' + hook + r'\b\s*[<(]', content):
            # Check if imported
            # import { useState } from 'react'
            # import { useQuery } from '@tanstack/react-query'
            if not re.search(r'import\s+.*?\b' + hook + r'\b', content):
                if not re.search(r'React\.' + hook, content):
                    missing.append(hook)
                    
    if missing:
        print(f"File: {filepath} missing imports: {', '.join(missing)}")

for root, dirs, files in os.walk('c:/Users/User/Desktop/clubs/clubs/msu_platform/frontend/src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            check_file(os.path.join(root, file))
