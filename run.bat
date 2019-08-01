cd "search engine app"
start npm run serve

cd ..

cd "search engine svc\src"
start npm start

set url="http://localhost:8080/"

start chrome %url%

exit