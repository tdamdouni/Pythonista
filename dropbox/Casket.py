#coding:utf-8

'''
Casket is Dropbox sync script for Pythonista.
https://github.com/sharkattack51/Pythonista

1) https://www.dropbox.com/developers/apps > Create app
2) Select the "Dropbox API app", "Files and datastores" and limited to ots own folder.
3) Enter your app name.
4) Get the "App key" and "App secret". edit the script.
'''

import datetime
import dropbox
import hashlib
import json
import os
import pprint
import webbrowser

pp = pprint.PrettyPrinter()

# Dropbox App設定
APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'
ACCESS_TYPE = 'app_folder'

# ディレクトリ設定
DIR_PYTHONISTA_DOCUMENTS = os.path.expanduser('~/Documents')
DIR_DROPBOX_SYNC_ROOT = os.path.join(DIR_PYTHONISTA_DOCUMENTS, 'Casket-Dropbox')
DIR_PREFERENCE = os.path.join(DIR_DROPBOX_SYNC_ROOT, '_pref')
FILE_DROPBOX_TOKEN = 'dropbox.token'
FILE_SYNCED_META = 'synced_meta.txt'

DEBUG = False 

# ファイルの同期処理
def sync_files(client, root_dir, synced_meta):
	
	# ディレクトリmeta情報を取得
	meta = {}
	try:
		meta = client.metadata(root_dir)
	except dropbox.rest.ErrorResponse as error:
		print error
		return
	
	for file_meta in meta['contents']:
		local_path = get_local_path(file_meta['path'])
		
		# ディレクトリ
		if file_meta['is_dir'] == True:
			if not os.path.exists(local_path):
				os.mkdir(local_path)
			sync_files(client, file_meta['path'], synced_meta)
		
		# ファイル
		else:
			
			# ローカルにファイルが無い場合はダウンロード
			if not os.path.exists(local_path):
				print 'file not found in the local. download the Dropbox file...'
				download(client, file_meta['path'], synced_meta)
				
			else:
				synced_file_meta = synced_meta[file_meta['path']]
				
				# ローカルファイルに更新があった場合はアップロード
				if synced_file_meta['md5'] != get_hash_md5(local_path):
					print 'local file is updated. upload the local file...'
					upload(client, file_meta['path'], synced_meta)
					
				# ローカルの更新日時が古い場合はダウンロード
				elif check_new_date(synced_file_meta['modified'], file_meta['modified']) == 1:
					print 'modified of Dropbox file is new. download the Dropbox file...'
					download(client, file_meta['path'], synced_meta)
					
				# ローカルのリビジョンが古い場合はダウンロード
				elif synced_file_meta['revision'] < file_meta['revision']:
					print 'revision of Dropbox file is new. download the Dropbox file...'
					os.remove(local_path)
					download(client, file_meta['path'], synced_meta)
	
	# ローカルファイルでクラウドに無い場合はアップロード
	for dir_path, dir_names, file_names in os.walk(DIR_DROPBOX_SYNC_ROOT):
		for file_name in file_names:
			path = os.path.join(dir_path, file_name)
			if DIR_DROPBOX_SYNC_ROOT in path and not DIR_PREFERENCE in path:
				path = path.split(DIR_DROPBOX_SYNC_ROOT)[1]
				if not path in synced_meta:
					print 'file not found in the Dropbox. upload the local file...'
					upload(client, path, synced_meta)
	
# ファイルのハッシュ値取得
def get_hash_md5(path):
	
	f = open(path, 'r')
	md5 = hashlib.md5(f.read()).hexdigest()
	f.close()
	return md5
	
# 更新日時確認
def check_new_date(str_date0, str_date1):
	
	format = '%a, %d %b %Y %H:%M:%S'
	date0 = datetime.datetime.strptime(str_date0.split(' +')[0], format)
	date1 = datetime.datetime.strptime(str_date1.split(' +')[0], format)
	if date0 > date1:
		return 0
	elif date0 < date1:
		return 1
	else:
		return 2
	
# ローカルパスに変換
def get_local_path(path):
	
	return os.path.join(DIR_DROPBOX_SYNC_ROOT, path[1:])

# ファイルのアップロード
def upload(client, path, synced_meta):
	
	print path
	
	f = open(get_local_path(path), 'r')
	meta = client.put_file(path, f, True)
	f.close()
	meta['md5'] = get_hash_md5(get_local_path(path))
	synced_meta[path] = meta

# ファイルのダウンロード
def download(client, path, synced_meta):
	
	print path
	
	f = open(get_local_path(path), 'w')
	response, meta = client.get_file_and_metadata(path)
	f.write(response.read())
	f.close()
	meta['md5'] = get_hash_md5(get_local_path(path))
	synced_meta[path] = meta

# 同期情報の保存
def save_synced_meta(synced_meta):
	
	if DEBUG:
		print 'meta data saved...'
		pp.pprint(synced_meta)
	
	synced_meta_path = os.path.join(DIR_PREFERENCE, FILE_SYNCED_META)
	f = open(synced_meta_path, 'w')
	json.dump(synced_meta, f)
	f.close()
		
# 前回同期情報の取得
def get_synced_meta():
	
	synced_meta = {}
	synced_meta_path = os.path.join(DIR_PREFERENCE, FILE_SYNCED_META)
	if os.path.exists(synced_meta_path):
		f = open(synced_meta_path, 'r')
		synced_meta = json.load(f)
		f.close()
	
	if DEBUG:
		print 'meta data opened...'
		pp.pprint(synced_meta)
	
	return synced_meta

# トークン認証処理
def process_oauth(session):
	
	token_path = os.path.join(DIR_PREFERENCE, FILE_DROPBOX_TOKEN)
	if not os.path.exists(token_path):
		
		# リクエストトークンの取得
		request_token = session.obtain_request_token()
		
		# アプリケーション許可
		print 'check the permission of the application...'
		url = session.build_authorize_url(request_token)
		webbrowser.open(url, True)
		print 'waiting for authentications of browser...'
		print 'press return...'
		raw_input()
		
		# 許可後にアクセスキーとシークレットを取得
		access_token = session.obtain_access_token(request_token)
		
		# トークンの保存
		f = open(os.path.join(DIR_PREFERENCE, FILE_DROPBOX_TOKEN), 'w')
		f.write('%s|%s' % (access_token.key, access_token.secret))
		f.close()
		
	else:
		
		# シリアライズデータからトークン情報を取得
		f = open(os.path.join(DIR_PREFERENCE, FILE_DROPBOX_TOKEN), 'r')
		accsess_key, accsess_secret = f.read().split('|')
		f.close()
		
		# セッションにトークン情報をセット
		session.set_token(accsess_key, accsess_secret)

def main():
	
	# ディレクトリの確認
	if not os.path.exists(DIR_DROPBOX_SYNC_ROOT):
		os.mkdir(DIR_DROPBOX_SYNC_ROOT)
	if not os.path.exists(DIR_PREFERENCE):
		os.mkdir(DIR_PREFERENCE)
		
	print 'Casket > Dropbox login...'
	
	# セッションを開始
	session = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	
	# トークン認証処理
	try: 
		process_oauth(session)
	except :
		print 'Login error...'
		return
	
	# クライアント作成
	client = dropbox.client.DropboxClient(session)
	print "Login:", client.account_info()['display_name']
	
	# 前回同期情報の取得
	synced_meta = get_synced_meta()
	
	# 同期処理
	print 'Casket > Dropbox sync start...'
	sync_files(client, '/', synced_meta)
	
	# 同期情報の保存
	save_synced_meta(synced_meta)
	
	print 'Casket > Dropbox sync finished...'

if __name__ == '__main__':
	main()
