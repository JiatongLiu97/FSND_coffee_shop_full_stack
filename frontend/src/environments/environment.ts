/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-4xm89r5o.us', // the auth0 domain prefix
    audience: 'coffe_shop_login', // the audience set for the auth0 app
    clientId: 'cAm6L1B1CxtZskB8zfK9W0SWSysoaW7p', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
