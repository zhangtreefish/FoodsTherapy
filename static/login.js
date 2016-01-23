(function(d, s, id) {
				  var js, fjs = d.getElementsByTagName(s)[0];
				  if (d.getElementById(id)) return;
				  js = d.createElement(s); js.id = id;
				  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.5&appId=511225495725100";
				  fjs.parentNode.insertBefore(js, fjs);
				}(document, 'script', 'facebook-jssdk'));

				function sendTokenToServer() {
                // console.log(FB.getLoginStatus()); undefined
                var access_token = FB.getAuthResponse()['accessToken'];
                console.log(access_token);
                // console.log(getLoginStatus()); TODO: not defined?
                // FB.api('/me',function(response) {
                //     console.log('Successful login at FB for:',response['name']);
                // });
                $.ajax({
                  type: 'POST',
                  url: '/fbconnect/?state={{STATE}}',//url points to the destination of request:server relaying the one-time code from client to the auth server g+
                  processData: false,//not to process into string
                  data: access_token,//:what is sent to the server is the one-time use code
                  contentType: 'application/octet-stream; charset=utf-8',
                  success: function(result) {
                    // Handle or verify the server response(i.e. result),passing to the client
                        $('#result').html(result);
                        if (result) { //result: additional info from server
                            $('#result').html(result);
                            $('#result').html('Login at FB Successful!</br>'+ result + '</br>Redirecting...');
                            setTimeout(function() {
                                window.location.href='/restaurants/';
                            }, 5000);
                        } else if (authResult['error']) {
                            console.log('There was an error: ' + authResult['error']);//report the error from google
                        } else {
                            $('#result').html('Failed to make a server-side call. Check your configuration and console.');// if no response from server to the callback
                        }
                    }//success
                });//ajax

                console.log('signed in via FB!');
            }
            function statusChangeCallback(response) {
                console.log('statusChangeCallback');
                console.log(response);
                // The response object is returned with a status field that lets the
                // app know the current login status of the person.
                // Full docs on the response object can be found in the documentation
                // for FB.getLoginStatus().
                if (response.status === 'connected') {
                  // Logged into your app and Facebook.
                  var accessToken = response.authResponse.accessToken;
                  // testAPI();
                } else if (response.status === 'not_authorized') {
                  // The person is logged into Facebook, but not your app.
                  document.getElementById('status').innerHTML = 'Please log ' +
                    'into this app.';
                } else {
                  // The person is not logged into Facebook, so we're not sure if
                  // they are logged into this app or not.
                  document.getElementById('status').innerHTML = 'Please log ' +
                    'into Facebook.';
                }
              }

              // This function is called when someone finishes with the Login
              // Button.  See the onlogin handler attached to it in the sample
              // code below.
            // function checkLoginState() {
            //     FB.getLoginStatus(function(response) {
            //       statusChangeCallback(response);
            //     });
            //   }


            window.fbAsyncInit = function() {
                // init:initialize and setup the SDK;
                // xfbml: whether XFBML tags used by social plugins are parsed; default to false
                // cookie: a cookie is created for the session and accessible by server-side code. TODO: when is it used?
                FB.init({
                    appId      : '511225495725100',
                    cookie     : true,
                    xfbml      : true,
                    version    : 'v2.5'
                });

                FB.getLoginStatus(function(response) {
                    statusChangeCallback(response);
                });
            };


            //for google+ login and logout
            function signOut() {
                var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function () {
                    console.log('User signed out.');
                });
            }
            function onSignIn(authResult) {
                // if google sends back the right response with the one-time code
                if (authResult['code']) {
                    // Hide the sign-in button now that the user is authorized
                    $('#signInButton').attr('style', 'display: none');
                    $('#result').html(authResult['code']);
                    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
                    //.ajax handles the response from google to the client:one-time code to authorize the server and access token for client to access server from browser, and pass onto the server
                    $.ajax({
                      type: 'POST',
                      url: '/gconnect/?state={{STATE}}',//url points to the destination of request:server relaying the one-time code from client to the auth server g+
                      processData: false,//not to process into string
                      data: authResult['code'],//:what is sent to the server is the one-time use code
                      contentType: 'application/octet-stream; charset=utf-8',
                      success: function(result) { //if 200 from google API Server...
                        // Handle or verify the server response if necessary, pass to the client
                            $('#result').html(result);
                            if (result) { //result: additional info from server
                                $('#result').html(result);
                                $('#result').html('Login Successful!</br>'+ result + '</br>Redirecting...');
                                setTimeout(function() {
                                    window.location.href='/restaurants/';
                                }, 5000);
                            } else if (authResult['error']) {
                                console.log('There was an error: ' + authResult['error']);//report the error from google
                            } else {
                                $('#result').html('Failed to make a server-side call. Check your configuration and console.');// if no response from server to the callback
                            }
                        }//success
                    });//ajax
                }//if
                console.log('signed in!');
            }
            function onSignInFailure() {
                console.log("Sign In Failed");
            }