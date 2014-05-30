import re
from reviewboard.hostingsvcs.repository import RemoteRepository
from reviewboard.hostingsvcs.utils.paginator import (APIPaginator,
                                                     ProxyPaginator)
class GitHubAPIPaginator(APIPaginator):
    """Paginates over GitHub API list resources.

    This is returned by some GitHubClient functions in order to handle
    iteration over pages of results, without resorting to fetching all
    pages at once or baking pagination into the functions themselves.
    """
    start_query_param = 'page'
    per_page_query_param = 'per_page'

    LINK_RE = re.compile(r'\<(?P<url>[^>]+)\>; rel="(?P<rel>[^"]+)",? *')

    def fetch_url(self, url):
        """Fetches the page data from a URL."""
        data, headers = self.client.api_get(url, return_headers=True)

        # Find all the links in the Link header and key off by the link
        # name ('prev', 'next', etc.).
        links = dict(
            (m.group('rel'), m.group('url'))
            for m in self.LINK_RE.finditer(headers.get('Link', ''))
        )

        return {
            'data': data,
            'headers': headers,
            'prev_url': links.get('prev'),
            'next_url': links.get('next'),
        }


    def api_get(self, url, return_headers=False, *args, **kwargs):
        """Performs an HTTP GET to the GitHub API and returns the results.

        If `return_headers` is True, then the result of each call (or
        each generated set of data, if using pagination) will be a tuple
        of (data, headers). Otherwise, the result will just be the data.
        """

            if return_headers:
                return data, headers
            else:
                return data
    def api_get_list(self, url, start=None, per_page=None, *args, **kwargs):
        """Performs an HTTP GET to a GitHub API and returns a paginator.

        This returns a GitHubAPIPaginator that's used to iterate over the
        pages of results. Each page contains information on the data and
        headers from that given page.

        The ``start`` and ``per_page`` parameters can be used to control
        where pagination begins and how many results are returned per page.
        ``start`` is a 0-based index representing a page number.
        """
        if start is not None:
            # GitHub uses 1-based indexing, so add one.
            start += 1

        return GitHubAPIPaginator(self, url, start=start, per_page=per_page)

    def api_get_remote_repositories(self, api_url, owner, plan,
                                    start=None, per_page=None):
        url = api_url

        if plan.endswith('org'):
            url += 'orgs/%s/repos' % owner
        elif owner == self.account.username:
            # All repositories belonging to an authenticated user.
            url += 'user/repos'
        else:
            # Only public repositories for the user.
            url += 'users/%s/repos?type=all' % owner

        return self.api_get_list(self._build_api_url(url),
                                 start=start, per_page=per_page)

        url = '/'.join(api_paths)

        if '?' in url:
            url += '&'
        else:
            url += '?'

        url += 'access_token=%s' % self.account.data['authorization']['token']

        return url
    def get_remote_repositories(self, owner=None, plan=None, start=None,
                                per_page=None):
        """Return a list of remote repositories matching the given criteria.

        This will look up each remote repository on GitHub that the given
        owner either owns or is a member of.

        If the plan is an organization plan, then `owner` is expected to be
        an organization name, and the resulting repositories with be ones
        either owned by that organization or that the organization is a member
        of, and can be accessed by the authenticated user.

        If the plan is a public or private plan, and `owner` is the current
        user, then that user's public and private repositories or ones
        they're a member of will be returned.

        Otherwise, `owner` is assumed to be another GitHub user, and their
        accessible repositories that they own or are a member of will be
        returned.

        `owner` defaults to the linked account's username, and `plan`
        defaults to 'public'.
        """
        if owner is None:
            owner = self.account.username

        if plan is None:
            plan = 'public'

        if plan not in ('public', 'private', 'public-org', 'private-org'):
            raise InvalidPlanError(plan)

        url = self.get_api_url(self.account.hosting_url)
        paginator = self.client.api_get_remote_repositories(url, owner, plan,
                                                            start, per_page)

        return ProxyPaginator(
            paginator,
            normalize_page_data_func=lambda page_data: [
                RemoteRepository(self,
                                 repository_id=repo['id'],
                                 name=repo['name'],
                                 owner=repo['owner']['login'],
                                 scm_type='Git',
                                 path=repo['clone_url'],
                                 mirror_path=repo['mirror_url'],
                                 extra_data=repo)
                for repo in page_data
            ])
