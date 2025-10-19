import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antiragging.settings')
django.setup()

from core.models import College, Branch

print('🏫 Adding colleges...\n')

# 1. PUC College
try:
    puc = College.objects.create(
        name='Government PU College',
        address='Mysore, Karnataka'
    )
    print('✅ PUC College created!')

    # Add PUC branches
    Branch.objects.create(name='Science (PCMB)', college=puc)
    Branch.objects.create(name='Science (PCMC)', college=puc)
    Branch.objects.create(name='Commerce', college=puc)
    Branch.objects.create(name='Arts', college=puc)
    print('   ✅ Added 4 PUC branches\n')
except Exception as e:
    print(f'❌ PUC Error: {e}\n')

# 2. ITI College
try:
    iti = College.objects.create(
        name='Government ITI Mysore',
        address='Bannimantap, Mysore'
    )
    print('✅ ITI College created!')

    # Add ITI trades
    Branch.objects.create(name='Electrician', college=iti)
    Branch.objects.create(name='Fitter', college=iti)
    Branch.objects.create(name='Welder', college=iti)
    Branch.objects.create(name='COPA', college=iti)
    print('   ✅ Added 4 ITI trades\n')
except Exception as e:
    print(f'❌ ITI Error: {e}\n')

# 3. Polytechnic
try:
    poly = College.objects.create(
        name='Government Polytechnic College',
        address='Hebbal, Mysore'
    )
    print('✅ Polytechnic created!')

    # Add Diploma branches
    Branch.objects.create(name='Diploma in Computer Science', college=poly)
    Branch.objects.create(name='Diploma in Mechanical', college=poly)
    Branch.objects.create(name='Diploma in Civil', college=poly)
    Branch.objects.create(name='Diploma in ECE', college=poly)
    print('   ✅ Added 4 Diploma branches\n')
except Exception as e:
    print(f'❌ Polytechnic Error: {e}\n')

print('🎉 Done! Refresh your admin dashboard!')
