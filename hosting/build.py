from pathlib import Path
import shutil, subprocess
root=Path(__file__).resolve().parent.parent
subprocess.run(['python3',str(root/'hosting/render-pages.py'),'--check'],check=True)
out=root/'public'
if out.exists():raise SystemExit('public already exists; use a clean checkout for an immutable build')
out.mkdir()
allowed={'.html','.css','.js','.json','.xml','.txt','.png','.jpg','.jpeg','.webp','.svg','.ico','.woff','.woff2','.ttf','.mp4','.webmanifest'}
for source in root.rglob('*'):
 relative=source.relative_to(root)
 if any(part.startswith('.') or part in {'public','hosting','node_modules'} for part in relative.parts):continue
 if source.is_file() and source.suffix.lower() in allowed:
  target=out/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
# Stripe prohibited-category guard (Dave, 1 Nov 2026: donation soliciting is prohibited for the BMSG Stripe account).
# Fail closed: no public image can carry a payment link or the old "Support the sunshine" page again.
forbidden=('buy.stripe.com','donate.stripe.com','checkout.stripe.com','donate.html?from=','Support the sunshine','Monthly sunshine')
for built in sorted(out.rglob('*')):
 if built.is_file() and built.suffix.lower() in {'.html','.js','.css','.json','.xml','.txt','.webmanifest'}:
  text=built.read_text(encoding='utf-8',errors='replace').lower()
  hits=[f for f in forbidden if f.lower() in text]
  if hits:raise SystemExit('donation solicitation is not allowed on the public site: '+str(built.relative_to(out))+' contains '+', '.join(hits))
