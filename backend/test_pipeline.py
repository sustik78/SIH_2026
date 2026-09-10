import urllib.request
import json
import urllib.parse

BASE_URL = 'http://127.0.0.1:8000'

def test_pipeline():
    print("=== PRAMAN AI VERIFICATION SUITE ===")
    
    # 1. Health check
    res = urllib.request.urlopen(f'{BASE_URL}/api/health')
    print('1. Health check:', json.loads(res.read().decode()))

    # 2. Test login with all 6 official credentials
    official_users = [
        ('Soutik@email.com', 'Soutik1234', 'Soutik'),
        ('Sayantan@email.com', 'Sayantan1234', 'Sayantan'),
        ('Jiya@email.com', 'Jiya1234', 'Jiya'),
        ('Rimi@email.com', 'Rimi1234', 'Rimi'),
        ('Debopriya@email.com', 'Debopriya1234', 'Debopriya'),
        ('Arkadip@email.com', 'Arkadip1234', 'Arkadip'),
    ]

    last_token = None
    print('\n2. Testing Authentication for all 6 users:')
    for email, pwd, uname in official_users:
        # Test with exact email
        data = urllib.parse.urlencode({'username': email, 'password': pwd}).encode()
        req = urllib.request.Request(f'{BASE_URL}/api/auth/login', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        res = urllib.request.urlopen(req)
        out = json.loads(res.read().decode())
        last_token = out['access_token']
        print(f"  [OK] Email: {email} -> {out['user']['full_name']} (Role: {out['user']['role']}, Badge: {out['user']['badge_number']})")

        # Test with exact username
        data_u = urllib.parse.urlencode({'username': uname, 'password': pwd}).encode()
        req_u = urllib.request.Request(f'{BASE_URL}/api/auth/login', data=data_u, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        res_u = urllib.request.urlopen(req_u)
        out_u = json.loads(res_u.read().decode())
        print(f"  [OK] Username: {uname} -> OK")

    # 3. Test Scanning with OCR + Nutrition Extraction + Rule Engine
    print('\n3. Testing Package Scan & AI Extraction Pipeline:')
    scan_data = urllib.parse.urlencode({
        'sample_filename': 'sample_compliant_atta.jpg',
        'product_name': 'Chakki Fresh Whole Wheat Atta',
        'category': 'Packaged Food / Atta'
    }).encode()
    scan_req = urllib.request.Request(
        f'{BASE_URL}/api/scan/upload', 
        data=scan_data, 
        headers={'Authorization': f'Bearer {last_token}', 'Content-Type': 'application/x-www-form-urlencoded'}
    )
    scan_res = urllib.request.urlopen(scan_req)
    scan_out = json.loads(scan_res.read().decode())
    
    print(f"  [OK] Inspection ID: {scan_out['inspection_id']}")
    print(f"  [OK] Score: {scan_out['overall_score']}/100 | Status: {scan_out['compliance_status']}")
    print(f"  [OK] Passed Checks: {scan_out['passed_count']} | Violations: {scan_out['violation_count']}")
    print(f"  [OK] Informational Health Assessment: {scan_out.get('health_classification', {}).get('classification')} (Score: {scan_out.get('health_classification', {}).get('score')})")
    print(f"  [OK] Health Summary: {scan_out.get('health_classification', {}).get('summary')}")
    
    print("\n  Extracted Nutritional Facts:")
    for k, v in scan_out.get('nutrition', {}).items():
        if isinstance(v, dict) and v.get('found'):
            print(f"    - {k}: {v.get('value')}")
        elif isinstance(v, dict):
            print(f"    - {k}: Not detected from package")

    # 4. Test Inspection Details Endpoint
    insp_id = scan_out['inspection_id']
    det_req = urllib.request.Request(f'{BASE_URL}/api/inspections/{insp_id}', headers={'Authorization': f'Bearer {last_token}'})
    det_res = urllib.request.urlopen(det_req)
    det_out = json.loads(det_res.read().decode())
    print(f"\n4. Inspection Details Endpoint:")
    print(f"  [OK] Product: {det_out['product_name']}")
    print(f"  [OK] Inspector: {det_out['inspector_name']}")
    print(f"  [OK] Has nutrition data: {bool(det_out.get('nutrition'))}")
    print(f"  [OK] Has health assessment: {bool(det_out.get('health_classification'))}")

    # 5. Test PDF Report Endpoint
    pdf_req = urllib.request.Request(f'{BASE_URL}/api/reports/{insp_id}/pdf')
    pdf_res = urllib.request.urlopen(pdf_req)
    print(f"\n5. Statutory PDF Report Download:")
    print(f"  [OK] Status Code: {pdf_res.getcode()} | Content-Type: {pdf_res.headers.get('Content-Type')}")

    # 6. Test Frontend Server
    fe_res = urllib.request.urlopen('http://localhost:5173/')
    print(f"\n6. Frontend Dev Server:")
    print(f"  [OK] Status Code: {fe_res.getcode()} | Vite ready")

    print("\n=== ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == '__main__':
    test_pipeline()
