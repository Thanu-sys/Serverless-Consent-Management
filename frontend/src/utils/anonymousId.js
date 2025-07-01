import { v4 as uuidv4 } from 'uuid';

export function getAnonymousUserId() {
  let userId = localStorage.getItem('anonymous_user_id');
  if (!userId) {
    userId = uuidv4();
    localStorage.setItem('anonymous_user_id', userId);
  }
  return userId;
}