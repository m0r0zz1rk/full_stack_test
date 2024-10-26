import {delCookie, getCookie} from "./cookie.js";
import {showAlert} from "./alerts.js";

// Запросы к backend через fetch
export function apiRequest (
  endpoint,
  method,
  body
) {
  // Функция для обращений к backend
  const backendUrl = import.meta.env.VITE_BACKEND_URL
  let csrfToken = getCookie('csrftoken')
  let request_parameters = {
    'method': method,
    'headers': {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json'
    }
  }
  if (body) {
    request_parameters['body'] = JSON.stringify(body)
  }
  return fetch(backendUrl+endpoint, request_parameters)
    .catch(e => {return null})
    .then(resp => {
      if ([401, 403].includes(resp.status)) {
        delCookie('cokoToken')
        showAlert(
          'error',
          'Авторизация',
          'Пожалуйста, войдите в систему'
        )
        window.location.replace('/login')
      }
      if(!([200, 201, 202, 204, 400, 401, 403, 404, 409, 500].includes(resp.status))) {
        showAlert(
          'error',
          'Ошибка запроса',
          'Произошла непредвиденная ошибка, повторите попытку позже'
        )
        return false
      } else {
        return resp.json()
      }
    })
    .then(data => (data))
}
