const API = {
  CREATE_URL: 'https://0mz8m03m21.execute-api.us-east-1.amazonaws.com/t/create',
};

let shortenedUrl = '';

function isUrlValid(url) {
  try {
    new URL(url);
    return true;
  } catch (error) {
    return false;
  }
}
const unsecuredCopyToClipboard = (text) => {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
  } catch (err) {
    console.error('Unable to copy to clipboard', err);
  }
  document.body.removeChild(textArea);
};

function copyToClipFn() {
  if (window.isSecureContext && navigator.clipboard) {
    navigator.clipboard.writeText(shortenedUrl);
  } else {
    unsecuredCopyToClipboard(shortenedUrl);
  }
  Toastify({
    text: 'Copied url to clipboard',
    position: 'center',
    className: 'info',
    duration: 3000,
  }).showToast();
}

function URLValidate() {
  var uRLVal = document.getElementById('search').value;
  var isValid = isUrlValid(uRLVal);

  if (isValid) {
    console.log('Link/URL is Valid');

    $('#loader').show();
    $('#output').hide();
    $('#error').hide();
    shortenedUrl = '';

    $.ajax({
      url: API.CREATE_URL,
      method: 'POST',
      timeout: 0,
      headers: {
        'Content-Type': 'application/json',
      },
      data: JSON.stringify({
        originalURL: uRLVal,
      }),
    })
      .fail(function (error) {
        console.log('Error occured', error);
        $('#error').html('Something wrong had happened. Please try again.');
        $('#error').show();
        $('#loader').hide();
      })
      .done(function (response) {
        console.log('got the url', response);
        shortenedUrl = response.shortURL;
        $('#formattedUrl').html(
          `<a href="${shortenedUrl}" target="_blank">${shortenedUrl}</a>`
        );
        $('#loader').hide();
        $('#output').show();
      });
  } else {
    console.log('Invalid Link/URL', uRLVal);

    //Show Error Div | Hide Output
    $('#output').hide();
    $('#error').show();

    $('#error').html('Invalid URL');
  }
}

/**
 * Called on keypress
 */
function clearOutput() {
  $('#output').hide();
  $('#error').hide();
}
