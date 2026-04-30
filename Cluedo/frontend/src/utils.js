export const getUrl = (path) => window.location.pathname.startsWith('/static/') ? '/static/' + (path.startsWith('/') ? path.substring(1) : path) : path;
