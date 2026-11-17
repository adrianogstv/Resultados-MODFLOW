"""Reconstruye el visor y verifica sus840 archivos sin conocer la contraseña. No publica."""
from pathlib import Path, PurePosixPath
import argparse,datetime,hashlib,json,shutil,zipfile
R=Path(__file__).resolve().parents[2]
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(8*1024*1024):h.update(b)
    return h.hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--salida',help='Carpeta NUEVA dentro de03 Output; por defecto se crea con fecha/hora.');a=p.parse_args()
    out=Path(a.salida) if a.salida else Path('03 Output')/('PUBLICACION_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    if not out.is_absolute():out=R/out
    out=out.resolve();allowed=(R/'03 Output').resolve()
    if not out.is_relative_to(allowed):raise ValueError('La salida debe estar en03 Output de este repositorio.')
    if out.exists():raise FileExistsError('Conservar resultados anteriores; use una salida nueva.')
    mf=json.loads((R/'02 Input/publicacion/MANIFIESTO.json').read_text(encoding='utf8'))
    # Validate all parts before writing any output.
    for item in mf['parts']:
        part=R/item['path']
        if not part.is_file() or part.stat().st_size!=item['size'] or digest(part)!=item['sha256']:raise ValueError('Parte cifrada ausente o modificada: '+item['path'])
    out.mkdir(parents=True);dist=out/'dist';dist.mkdir()
    archive=out/'recursos_cifrados.zip'
    with archive.open('xb') as target:
        for item in mf['parts']:
            with (R/item['path']).open('rb') as src:shutil.copyfileobj(src,target)
    if digest(archive)!=mf['archive_sha256']:raise ValueError('ZIP cifrado no coincide con el manifiesto.')
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            rel=PurePosixPath(member.filename)
            if rel.is_absolute() or '..' in rel.parts or member.is_dir() or rel.suffix!='.bin':raise ValueError('Miembro inesperado: '+member.filename)
            destination=(dist/Path(*rel.parts)).resolve()
            if not destination.is_relative_to(dist):raise ValueError('Ruta fuera de dist.')
            destination.parent.mkdir(parents=True,exist_ok=True)
            with z.open(member) as src,destination.open('xb') as target:shutil.copyfileobj(src,target)
    for name in ['index.html','app.js','app.css']:shutil.copy2(R/'00 Code/visor'/name,dist/name)
    shutil.copy2(R/'02 Input/publicacion/crypto.json',dist/'crypto.json')
    for item in mf['files']:
        f=dist/item['path']
        if not f.is_file() or f.stat().st_size!=item['size'] or digest(f)!=item['sha256']:raise ValueError('Archivo web modificado: '+item['path'])
    actual={f.relative_to(dist).as_posix() for f in dist.rglob('*') if f.is_file()}
    if actual!={v['path'] for v in mf['files']}:raise ValueError('Archivos adicionales o faltantes en dist.')
    (out/'.openai').mkdir();shutil.copy2(R/'.openai/hosting.json',out/'.openai/hosting.json')
    (out/'VERIFICACION.json').write_text(json.dumps({'status':'PASS','files':len(actual),'bytes':sum(v['size'] for v in mf['files']),'password_required_for_build':False,'decrypted_files':0,'deployed':False,'site_id':'appgprj_6adb901106488191aff5c0d1a12199f7'},indent=2),encoding='utf8')
    print('READY',out);print('Abrir con HTTP en localhost o HTTPS; la publicación sigue siendo un paso separado.')
if __name__=='__main__':main()
