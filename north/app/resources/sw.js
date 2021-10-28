base_url = 'north/' // Needs to be templated

// I store the path with the prefix of /container.
// Returns a path as string
function extractPath(url) {
  return url.match(/\/container\/[0-9]+/g)[0];
}

function getIndexedDB() {
    return new Promise((resolve,reject) => {
      var dbRequest = indexedDB.open('nomad-north', 1)
      dbRequest.onsuccess = (event) => {
        resolve(event.target.result)
      }
    })
  }

function getToken(db, path) {
    return new Promise((resolve,reject) => {
        var tx = db.transaction(['tokens'], 'readwrite')
        var store = tx.objectStore('tokens')
        store.getAll().onsuccess = (event) => {
            event.target.result.forEach(element => {
                if (element.path == path)
                    resolve(element.channel_token)
            });
            resolve('')
        }
    })
}

async function customHeaderRequestFetch(event) {
    if (event.request.url.includes(base_url + 'sw-installed'))
      return new Response('Installed')

    if (event.request.url.includes(base_url + 'instances')) {
        response = await fetch(event.request)
        respClone = response.clone()
        response.json().then((json) => {
            // store the token
            var dbRequest = indexedDB.open('nomad-north', 1)
            dbRequest.onsuccess = (event) => {
            db = event.target.result
            var tx = db.transaction(['tokens'], 'readwrite')
            var store = tx.objectStore('tokens')
            store.clear()
            let path = extractPath(json['path'])
            store.add({path:path, channel_token:json['channel_token']})
            }
        })
        return respClone
    }
    if (event.request.url.includes(base_url + 'container'))
    {
        // Strip the path with channel id and find the token from the store
        db = await getIndexedDB()
        token = await getToken(db, extractPath(event.request.url))

        let reqheaders = {}
        for (const [header, value] of event.request.headers) {
            reqheaders[header] = value
        }

        reqheaders['Authorization'] = 'Bearer ' + token

        reqbody = ''
        // Get requests cannot have body
        if (event.request.method == 'GET')
        reqbody = undefined;
        // if json do the following:
        if((typeof reqheaders['content-type'] !== 'undefined') && ((reqheaders['content-type'] == 'application/json') || (reqheaders['content-type'].substr(0,10) == 'text/plain')))
        {
        reqbody = JSON.stringify(await event.request.clone().json().catch((err) => err))
        }
        // if application/x-www...:
        else if((typeof reqheaders['content-type'] !== 'undefined') && (reqheaders['content-type'].substr(0, 33) == 'application/x-www-form-urlencoded'))
        {
        reqbody = await event.request.clone().text().catch((err) => err)
        }

        const newRequest = new Request(event.request.url.toString(), {
            method: event.request.method,
            headers: reqheaders,
            body: reqbody,
            mode: 'cors',
            credentials: event.request.credentials,
            cache: event.request.cache,
            redirect: event.request.redirect,
            referrer: event.request.referrer,
            referrerPolicy: event.request.referrerPolicy,
            integrity: event.request.integrity,
            keepalive: event.request.keepalive,
            signal: event.request.signal
          })
          return fetch(newRequest)
    }

    return fetch(event.request)

}

self.addEventListener('fetch', (event) => {
    event.respondWith(
      customHeaderRequestFetch(event)
    );
  });

function createDB() {
    var dbRequest = indexedDB.open('nomad-north', 1)
    dbRequest.onupgradeneeded = (event) => {
      db = event.target.result
      db.createObjectStore('tokens', {keyPath: 'channel_token'});
    }
}

self.addEventListener('activate', function(event) {
event.waitUntil(
    createDB()
);
});