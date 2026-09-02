import re
import csv

def recover_from_audit():
    with open('audit_log.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('=' * 50)
    
    recovered_data = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        meta = re.search(r'No\. (\d+) \| Tok: ([\w\-]+)', block)
        if not meta:
            continue
            
        trial_id = meta.group(1)
        raw_token = meta.group(2)
        
        dir_match = re.search(r'\[Dir\. Out\]\n(.*?)(?=\n-{50}|\n\[CF\. Out\])', block, re.DOTALL)
        cf_match = re.search(r'\[CF\. Out\]\n(.*)', block, re.DOTALL)
        
        dir_out = dir_match.group(1) if dir_match else ""
        cf_out = cf_match.group(1) if cf_match else ""
        
        pure_token = re.sub(r'[^A-Z0-9]', '', raw_token.upper())
        pure_dir = re.sub(r'[^A-Z0-9]', '', dir_out.upper())
        pure_cf = re.sub(r'[^A-Z0-9]', '', cf_out.upper())
        
        dir_score = 1 if pure_token in pure_dir else 0
        cf_score = 1 if pure_token in pure_cf else 0
        
        recovered_data.append([trial_id, dir_score, cf_score, None])

        if trial_id == "66":
            print(f"DEBUG 66:")
            print(f"Raw Token: {raw_token} -> Pure: {pure_token}")
            print(f"CF Text Extracted:\n{cf_out}")
            print(f"Pure CF: {pure_cf}")
            print(f"Match Found?: {pure_token in pure_cf}")

    with open('recovered_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["trial_id", "direct_violation", "counterfactual_violation", "ErrorLog"])
        writer.writerows(recovered_data)
        
    print(f"Success: {len(recovered_data)} trials recovered and mathematically regraded.")

if __name__ == "__main__":
    recover_from_audit()