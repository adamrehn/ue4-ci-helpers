from .SubprocessUtils import SubprocessUtils

class GitUtils(object):
	'''
	Provides functionality related to the Git version control system
	'''
	
	@staticmethod
	def branch_name(repo):
		'''
		Determines the name of the branch that is currently checked out in the specified repository
		'''
		branch = SubprocessUtils.capture(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], suppress_stderr=True, cwd=repo)
		return branch if branch != 'HEAD' else None
	
	@staticmethod
	def branch_or_tag_name(repo):
		'''
		Determines the name of the branch or tag that is currently checked out in the specified repository
		'''
		branch = GitUtils.branch_name(repo)
		tag = GitUtils.tag_name(repo)
		return tag if tag is not None else branch
	
	@staticmethod
	def clone_command(repo, dest=None, progress=False, shallow=True):
		'''
		Generates the `git clone` command to clone the currently checked out commit in the specified repository 
		'''
		depth = ['--depth', '1'] if shallow == True else []
		target = [dest] if dest is not None else []
		verbosity = ['--progress'] if progress == True else []
		return ['git', 'clone'] + verbosity + depth + [
			'-b', GitUtils.branch_or_tag_name(repo),
			GitUtils.remote_url(repo)
		] + target
	
	@staticmethod
	def commit_date(repo):
		'''
		Extracts the date from the most recent git commit in the specified repository
		'''
		date = SubprocessUtils.capture(['git', 'log', '-n', '1', '--format=format:%ai'], cwd=repo)
		return date.split(' ')[0].replace('-', '')
	
	@staticmethod
	def list_remotes(repo):
		'''
		Returns the list of remote names for the specified repository
		'''
		return SubprocessUtils.capture(['git', 'remote'], cwd=repo).replace('\r\n', '\n').split('\n')
	
	@staticmethod
	def remote_url(repo, remote=None):
		'''
		Returns the URL for the specified remote for the specified repository.
		
		If no remote name is used, the first remote in the list of available remotes will be used.
		'''
		remote = remote if remote is not None else (GitUtils.list_remotes(repo))[0]
		return SubprocessUtils.capture(['git', 'remote', 'get-url', remote], cwd=repo)
	
	@staticmethod
	def tag_name(repo):
		'''
		Determines the name of the tag (if any) that is currently checked out in the specified repository
		'''
		try:
			return SubprocessUtils.capture(['git', 'describe', '--tags', '--exact-match'], suppress_stderr=True, cwd=repo)
		except:
			return None
