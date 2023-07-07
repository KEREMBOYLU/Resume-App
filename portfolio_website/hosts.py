from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'portfolio_website.urls', name=' '),
    host(r'admin', 'core.admin_urls', name='admin'),
)