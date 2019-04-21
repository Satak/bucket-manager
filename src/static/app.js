async function API(body, url, method) {
  const requestParams = {
    method: method,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }
  if (body) {
    requestParams['body'] = JSON.stringify(body)
  }

  const response = await fetch(url, requestParams)
  if (response.ok) return await response.json()
  const err = await response.json()
  throw new Error(err.error)
}

async function deleteFile(fileName) {
  const conf = confirm(`Do you want to delete the file: ${fileName}?`)
  if(!conf) {
    return null
  }
  const url = `/api/files?fileName=${fileName}`
  const requestParams = {
    method: 'DELETE'
  }
  const response = await fetch(url, requestParams)
  if (response.ok) {
    document.location.reload()
  } else {
    const err = await response.json()
    alert(err)
  }
}
