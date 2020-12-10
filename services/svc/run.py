from svc import app

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=app.config['PORT'], debug=True)
  ### app.run(host="0.0.0.0", port=8080, debug=True)
  ### app.run(ssl_context=('cert.pem', 'key.pem'), host="0.0.0.0", port=app.config['PORT'], debug=True)
