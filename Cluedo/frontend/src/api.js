export const getCsrfToken = () => {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

export const fetchCsrf = async () => {
  try {
    await fetch('/api/csrf/', { credentials: 'include' });
  } catch (error) {
    console.error('Error fetching CSRF:', error);
  }
};

export const postApi = async (url, data) => {
  let token = getCsrfToken();
  if (!token) {
    await fetchCsrf();
    token = getCsrfToken();
  }
  
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': token
    },
    credentials: 'include',
    body: JSON.stringify(data)
  });
};
