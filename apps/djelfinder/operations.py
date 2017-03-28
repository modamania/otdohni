# -*- coding: utf-8 -*-
import os
import settings
import hashlib
import re
from datetime import datetime
import mimetypes as mimes
from django.http import HttpResponse, Http404

#import Image
imglib = False
try:
	import Image
	imglib = True
except ImportError:
	pass

def file_size(f):
	return os.stat(f).st_size

def dir_size(path):
	total_size = 0
	if True:
            try:
		for dirpath, dirnames, filenames in os.walk(path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				if os.path.exists(fp):
					total_size += os.stat(fp).st_size
            except:
		total_size = os.lstat(path).st_size
	else:
		total_size = os.lstat(path).st_size
	return total_size


def hash(path):
	m = hashlib.md5()
        try:
            m.update(path)
        except UnicodeEncodeError:
            path = path.encode('utf8')
            m.update(path)

	return str(m.hexdigest())

def get_url(path):
	djelfinder_path = getattr(settings, 'DJELFINDER_ROOT', settings.MEDIA_ROOT)
	djelfinder_abspath = os.path.join(settings.MEDIA_ROOT, djelfinder_path)
	rel_path = os.path.relpath(path, djelfinder_abspath).replace('\\','/')
	abs_url = getattr(settings, 'DJELFINDER_URL', settings.MEDIA_URL)
        try:
            res = u'%s/%s'%(abs_url, rel_path)
        except UnicodeDecodeError:
            #import ipdb;ipdb.set_trace()
            #rel_path = rel_path.decode('utf8')
            res = '%s/%s'%(abs_url, rel_path)
	return res

def filtering(cwd):
	dirs = [os.path.join(cwd,d) for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]
	files = [os.path.join(cwd,f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
	u = []
	for d in dirs:
		l = []
		l.append(('name', os.path.basename(d)))
		l.append(('hash', hash(d)))
		l.append(('date', datetime.fromtimestamp(os.stat(d).st_mtime).strftime("%d %b %Y %H:%M")))
		l.append(('mime', 'directory'))
		l.append(('read', True))
		l.append(('write', True))
		l.append(('rm', True))
		l.append(('dirs', filtering(d)))
		u.append(dict(l))
	return u

def get_mime(path):
	mime = mimes.guess_type(path)[0] or 'Unknown'
	if mime.startswith('image/'):
		return mime, True
	return mime, False

def cdc(path):
	global imglib
	u = []
	dirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
	files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
	for d in dirs:
		l = {}
		l['name'] = os.path.basename(d)
		l['hash'] = hash(d)
		l['date'] = datetime.fromtimestamp(os.stat(d).st_mtime).strftime("%d %b %Y %H:%M")
		l['mime'] = 'directory'
		l['size'] = dir_size(d)
		l['read'] = True
		l['write'] = True
		l['rm'] = True
		u.append(l)
	#for files in cwd
	for f in files:
		l = {}
		l['name'] = os.path.basename(f)
		l['hash'] = hash(f)
		l['date'] = datetime.fromtimestamp(os.stat(f).st_mtime).strftime("%d %b %Y %H:%M")
		mime, is_image = get_mime(f)
		if is_image and imglib:
			try:
				img = Image.open(f)
				l['dim'] = '%dx%d'%img.size
				l['resize'] = True
				l['tmb'] = get_url(f)
				img.close()
			except:
				pass
		l['mime'] = mime
		l['size'] = file_size(f)
		l['read'] = True
		l['write'] = True
		l['rm'] = True
		l['url'] = get_url(f)
		u.append(l)
	return u

def check_name(name):
	pattren = r'[\/\\\:\<\>]'
	if re.search(pattren, name):
		return False
	return True

def cwd(path):
	d = {}
	time = 'Today'
	try:
		time = datetime.fromtimestamp(os.stat(path).st_mtime).strftime("%d %b %Y %H:%M")
	except:
		pass
	d['name'] = os.path.basename(path)
	d['hash'] = hash(path)
	d['rel'] = 'Home'
	d['date'] = time
	d['mime'] = 'directory'
	d['size'] = dir_size(path)
	d['read'] = True
	d['write'] = True
	d['rm'] = False

	return d

def tree():
	mr = getattr(settings, 'DJELFINDER_ROOT', settings.MEDIA_ROOT)
	t = {}
	t['name'] = os.path.basename(mr)
	t['hash'] = hash(mr)
	t['read'] = True
	t['write'] = True
	t['dirs'] = filtering(mr)
	return t
def find_path(fhash, cur=None):
	mr = cur or settings.MEDIA_ROOT
	fp = None
	for dirpath, dirnames, filenames in os.walk(mr):
		for f in filenames:
			f = os.path.join(dirpath, f)
			if fhash == hash(f):
				fp = f
				#raise ValueError, fp
				return fp
		for d in dirnames:
			d = os.path.join(dirpath, d)
			if fhash == hash(d):
				fp = d
				#raise ValueError, d
				return fp

	return fp

def rename(target, current, name):
	err = {}
	if not check_name(name):
		err['error'] = u'Invalid name'
		return err
	if not target or not os.path.exists(target):
		if os.path.exists(os.path.join(current, name)):
			return hash(os.path.join(current, name))
		err['error'] = u'Invalid parameters'
		return err
	try:
		os.rename(target, os.path.join(current,name))
		return hash(os.path.join(current, name))
	except:
		err['error'] = u'file or folder cannot renamed'
	return None

def force_remove(dir):
	#remove the directory even is its not empty
	for curdir, dirs, files in os.walk(dir):
		for f in files:
			print 'FILE::%s'%files
			os.remove(os.path.join(curdir, f))
		for d in dirs:
			d = os.path.join(curdir, d)
			print 'DIR::%s -- FILES::%s'%(d, files)
			if not os.listdir(d):
				os.rmdir(d)
		#and finally remove the current folder
		if not os.listdir(curdir):
			os.rmdir(curdir)
	#then remove our folder
	#os.rmdir(dir)
	return True

def get_targets(request):
	targets = [s[14:] for s in request.get_full_path().rsplit('?',1)[1].split('&') if s.startswith('targets')]
	targets = [find_path(target) for target in targets]
	return targets

def remove(targets, current):
	err = {}
	for target in targets:
		if not target:
			continue
		path = os.path.join(current, target)
		if not os.path.exists(path): continue
		try:
			os.remove(path)
		except:
			try:
				os.rmdir(path)
			except Exception, e:
				if os.path.isdir(path): #dirctory is not empty !
					try:
						if force_remove(path):
							try:
								os.rmdir(path)
							except:
								pass
							continue
					except Exception, e: #badly habits
					#	raise
						err['error'] = '%s cannot be removed %s'%(os.path.basename(path), e)
						return err
	return True

def make_directory(current, name):
	err = {}
	if not check_name(name):
		err['error'] = u'Invalid name'
		return err
	new_dir = os.path.join(current, name)
	if os.path.exists(new_dir):
		err['error'] = u'file or folder with the same name already exists'
		return err
	try:
		os.mkdir(new_dir)
		return hash(new_dir)
	except:
		err['error'] = u'Unable to create folder'
		return err
	return False

def make_file(current, name):
	err = {}
	if not check_name(name):
		err['error'] = u'Invalid name'
		return err
	new_file = os.path.join(current, name)
	if os.path.exists(new_file):
		err['error'] = u'file or folder with the same name already exists'
		return err
	try:
		open(new_file, 'w').close()
		return hash(new_file)
	except:
		err['error'] = u'Unable to create file'
		return err
	return False

def safe_copy(src, dst):
	import shutil
	if os.path.isfile(src):
		try:
			shutil.copyfile(src, dst)
			shutil.copymode(src, dst)
			return True
		except:
			return False
	elif os.path.isdir(src):
		try:
			os.mkdir(dst)
		except:
			return False
		for f in os.listdir(src):
			new_src = os.path.join(src, f)
			new_dist = os.path.join(dst, f)
			if not safe_copy(new_src, new_dist):
				return False
	return True
def paste(current, src, dst, targets, cut=None):
	err = {}
	for target in targets:
		if not target:
			err['error'] = u'file not found !'
			return err
		new_dist = os.path.join(dst, os.path.basename(target))
		if dst.find(target) == 0:
			err['error'] = u'Unable to copy into itself'
			return err
		if os.path.exists(new_dist):
			err['error'] = u'file or folder with the same name "%s" already exists'%os.path.basename(new_dist)
			return err
		if cut:
			try:
				os.rename(target, new_dist)
				continue
			except:
				err['error'] = u'Unable to move files :) !'
				return err
		else:
			try:
				if safe_copy(target, new_dist):
					continue
				else:
					err['error'] = u'Unable to copy files !'
					return err
			except Exception, e:
				err['error'] = u'Unable to copy "%s" into new distnation --%s--'%(os.path.basename(target), e)
				return err
	return True

def unique_name(target, copy=' copy'):
	current_directory = os.path.dirname(target)
	target_name = os.path.basename(target)
	last_dot = target_name.rfind('.')
	ext = new_name = ''
	if not os.path.isdir(target) and re.search(r'\..{3}\.(gz|bz|bz2)$', target_name):
		pos = -7
		if target_name[-1:] == '2': #found .bz2 in ext
			pos -= 1
		ext = target_name[pos:]
		old_name = target_name[0:pos]
		new_name = old_name + copy
	elif os.path.isdir(target) or last_dot <= 0:
		old_name = target_name
		new_name = old_name + copy
	else:
		ext = target_name[last_dot:]
		old_name = target_name[0:last_dot]
		new_name = old_name + copy

	pos = 0

	if old_name[-len(copy):] == copy:
		new_name = old_name
	elif re.search(r''+copy+'\s\d+$', old_name):
		pos = old_name.rfind(copy) + len(copy)
		new_name = old_name[0:pos]
	else:
		new_path = os.path.join(current_directory, new_name+ext)
		if not os.path.exists(new_path):
			return new_path

	#if we are here then copy already exists or making copy of copy
	#we'll make new indexed copy * Black Magic*
	idx = 1
	if pos > 0: idx = int(old_name[pos:])
	while True:
		idx += 1
		new_name_ext = new_name + ' ' + str(idx) + ext
		new_path = os.path.join(current_directory, new_name_ext)
		if not os.path.exists(new_path):
			return new_path
	return

def duplicate(target, current):
	err = {}
	new_name = unique_name(target)
	if not safe_copy(target, new_name):
		err['error'] = u'Unable to create file copy'
		return err
	return True

def edit(target, current, content):
	err = {}
	try:
		f = open(target, 'wb')
		f.write(content)
		f.close()
		return hash(target)
	except:
		err['error'] = u'Unable to write to the file'
		return err
	return err

def reader(target, current):
	err = {}
	try:
		f = open(target, 'read')
		con = f.read()
		f.close()
		a={'a':"con"}
		from django.utils import simplejson as json
		#try to encodong contents well
		y = json.dumps(a)
		return con
	except UnicodeDecodeError:
		err['error'] = u'Unable to open file [file encoding not supported]'
		return err
	except:
		err['error'] = u'unable to open file'
		return err
	return True

def build_tar_archive(current, new_archive, targets, gzip=False, bzip2=False):
	import tarfile as tar
	err = {'error':'Not supported archive type'}
	curdir = os.getcwd()
	os.chdir(current)
	mode = 'w'
	if gzip:
		mode = 'w:gz'
	elif bzip2:
		mode = 'w:bz2'
	new_tar = tar.open(os.path.basename(new_archive), mode=mode)
	for target in targets:
		target = os.path.basename(target)
		new_tar.add(target, arcname=target)
	new_tar.close()
	os.chdir(curdir)
	return new_archive

def build_zip_archive(current, new_archive, targets):
	import zipfile
	err = {}
	curdir = os.getcwd()
	os.chdir(current)
	new_zip = zipfile.ZipFile(new_archive, mode='w')
	for target in targets:
		if os.path.isfile(target):
			new_zip.write(target, arcname=os.path.basename(target))
			continue
		elif os.path.isdir(target):
			for cdir, dirs, files in os.walk(target):
				print cdir
				#if not os.path.basename(cdir) in targets :
				for f in files:
					fp = os.path.join(cdir, f)
					fd = os.path.relpath(fp, start=current).replace('\\', '/')
					new_zip.write(fp, arcname=fd)
	new_zip.close()
	os.chdir(curdir)
	return new_archive

def archive(current, arch_type, targets, name):
	err = {}
	extensions = {
		'application/zip':'.zip',
		'application/x-tar':'.tar',
		'application/x-7z-compressed':'.7z',
		'application/x-gzip':'.tar.gz',
		'application/x-bzip2':'.tar.bz2'
		}

	new_archive = os.path.join(current, name)
	ext = extensions[arch_type]
	path = None
	if ext:
		new_archive += ext
	else:
		err['error'] = u'Unkown Archive type'
		return err
	if os.path.exists(new_archive):
		err['error'] = u'Archive with the name of "%s" already exists'%os.path.basename(new_archive)
		return err

	if ext == '.tar':
		path = build_tar_archive(current, new_archive, targets)
	elif ext == '.zip':
		path = build_zip_archive(current, new_archive, targets)
	elif ext == '.tar.bz2':
		path = build_tar_archive(current, new_archive, targets, bzip2 = True)
	elif ext == '.tar.gz':
		path = build_tar_archive(current, new_archive, targets, gzip=True)
	else:
		err['error'] = u'Not Supported Archive type'
		return err
	return path

def extract_tar(target, current, zip=False):
	tar = None
	if not zip:
		import tarfile
		tar = tarfile.open(target)
	else:
		import zipfile
		tar = zipfile.ZipFile(target)
	try:
		tar.extractall(path=current)
	except:
		return False
	return True

def extract(target, current):
	'''Extract target archive'''
	err = {}
	extracters = {
		'.tar':extract_tar,
		'.gz':extract_tar,
		'.bz2':extract_tar,
		'.zip':extract_tar,
		}
	arcname = os.path.basename(target)
	ext = os.path.splitext(arcname)[1]
	if not ext in extracters:
		err['error'] = 'unsupported archive type'
		return err
	zip = {'zip':False}
	if ext == '.zip':
		zip = {'zip':True}
	extract_method = extracters[ext]
	extracted = apply(extract_method, (target, current), zip)
	return extracted




def run(request, target=settings.MEDIA_ROOT, cmd='open', init=True, current=None):
	mr = target or (getattr(settings, 'DJELFINDER_ROOT', None) or settings.MEDIA_ROOT)
	out = {}
	trees = []
	try:
		trees = tree()
	except:
		pass
	if cmd == 'extract':
		if not target or not current:
			out['error'] = u'Invalid parameters'
			mr = current or mr
		else:
			extracted = extract(target, current)
			if isinstance(extracted, dict):
				out.update(extracted)
			if not extracted:
				out['error'] = u'Unable to extract file'
			mr = current or mr
	if cmd == 'archive':
		name = request.GET.get('name', None)
		typ = request.GET.get('type', None)
		#raise ValueError, typ
		targets = get_targets(request)
		if not (current and typ and targets and name):
			out['error'] = u'Invalid parameters'
			mr = current or mr
		else:
			archived = archive(current, typ, targets, name)
			if isinstance(archived, dict):
				out.update(archived)
			else:
				out['select'] = hash(archived)
			mr = current or mr
	if cmd == 'edit':
		content = request.POST.get('content', '')
		edited = edit(target, current, content)
		if isinstance(edited, dict):
			out.update(edited)
			mr = current or mr
		else:
			out['target'] = edited
			mr = current or mr
	if cmd == 'read':
		if current and target:
			read = reader(target, current)
			if isinstance(read, dict):
				out.update(read)
			else:
				out['content'] = read
			mr = current
		else:
			out['error'] = u'Invalid parameters'
			mr = current
	if cmd == 'duplicate':
		if not current:
			out['error'] = u'Invalid parameters'
			mr = current or mr
		else:
			if not target:
				target = current
			duplicated = duplicate(target, current)
			if isinstance(duplicated, dict):
				out.update(duplicated)
			mr = current or mr
	if cmd == 'paste':
		targets = get_targets(request)
		src = request.GET.get('src', None)
		dst = find_path(request.GET.get('dst', None))
		cut = request.GET.get('cut', None)
		if not current or not src or not dst or not targets:
			out['error'] = u'Invalid parameters !'
			mr = current or mr
		else:
			pasted = paste(current, src, dst, targets, cut=(cut == '1'))
			if isinstance(pasted, dict):
				out.update(pasted)
			mr = current or mr
	if cmd == 'mkfile':
		made = make_file(current, request.GET.get('name', None))
		if isinstance(made, dict):
			out.update(made)
			mr = current
		else:
			out['select'] = made
			mr = current
	if cmd == 'mkdir':
		made = make_directory(current, request.GET.get('name', None))
		if isinstance(made, dict):
			out.update(made)
			mr = current
		else:
			out['select'] = made
			mr = current
	if cmd == 'rm':
		targets = get_targets(request)
		removed = remove(targets, current)
		if not removed:
			mr = current
			out['error'] = 'failed to remove files'
			out['select'] = hash(current)
		else:
			if isinstance(removed, dict) and removed.has_key('error'):
				out.update(removed)
			mr = current
	if cmd == 'rename':
		renamed = rename(target, current, request.GET.get('name', None))
		if isinstance(renamed, dict):
			out.update(renamed)
			mr = current
		else:
			target = os.path.join(current, request.GET.get('name', None))
			out['select'] = hash(target)
			mr = current
	#FF = filtering(mr)
	out.update( {
		"cwd":cwd(mr),
		"cdc": cdc(mr),
		"tree":trees,
		"disabled"  : [],
		"tmb":True,
		"params"    : {
			"url"        : "http://localhost/connector/",
			"dotFiles"   : True,
			"uplMaxSize" : "15M",
			"extract"    : [
				   "application/x-7z-compressed",
				   "application/x-tar",
				   "application/x-gzip",
				   "application/x-bzip2",
				   "application/zip",
				   "application/x-rar",
			],
			"archives"   : [
				   "application/x-7z-compressed",
				   "application/x-tar",
				   "application/x-gzip",
				   "application/x-bzip2",
				   "application/zip",
				   "application/x-rar",
			]
     }


	})

	return out
