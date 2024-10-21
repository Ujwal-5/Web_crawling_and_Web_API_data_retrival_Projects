<?php
// Load necessary libraries
require 'vendor/autoload.php'; // Assuming you have Guzzle installed via Composer
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

// Create a Guzzle HTTP client session
$client = new Client([
    'cookies' => true, // Enable cookies
]);

try {
    // Make a GET request to the home page
    $homeResponse = $client->get('https://www.business.gov.om/portal/searchEstablishments?locale=en');
    $homeHtml = (string) $homeResponse->getBody();

    // Use regex to find the captcha token in the HTML
    preg_match('/\/portal\/botdetectcaptcha\?get=image&amp;c=exampleCaptcha&amp;t=([a-f0-9]+)/', $homeHtml, $matches);

    if (!empty($matches)) {
        $captchaToken = $matches[1];
        echo "Captcha Token: $captchaToken\n";
    } else {
        echo "No match found\n";
    }

    // Get the captcha image using the token found
    $captchaResponse = $client->get("https://www.business.gov.om/portal/botdetectcaptcha?get=image&c=exampleCaptcha&t=$captchaToken");
    $captchaContent = $captchaResponse->getBody()->getContents();

    // Encode the captcha image to Base64 for solving
    $base64Image = base64_encode($captchaContent);

    // Use 2Captcha API to solve the captcha
    $apiKey = getenv('APIKEY_2CAPTCHA') ?: 'your_2captcha_key';
    $solverResponse = $client->post('http://2captcha.com/in.php', [
        'form_params' => [
            'key' => $apiKey,
            'method' => 'base64',
            'body' => $base64Image,
            'json' => 1,
        ]
    ]);

    $solverData = json_decode($solverResponse->getBody(), true);
    $captchaId = $solverData['request'];

    // Poll for the result
    sleep(20); // Wait for 2Captcha to process

    $captchaResultResponse = $client->get("http://2captcha.com/res.php?key=$apiKey&action=get&id=$captchaId&json=1");
    $resultData = json_decode($captchaResultResponse->getBody(), true);

    if ($resultData['status'] == 1) {
        $captchaValue = $resultData['request'];
        echo "Captcha Value: $captchaValue\n";
    } else {
        echo "Captcha solving failed.\n";
    }

    // Extract additional tokens from HTML
    preg_match('/id="BDC_SP_exampleCaptcha" name="BDC_SP_exampleCaptcha" value="([a-f0-9]+)"/', $homeHtml, $matches);
    $BDC_SP_exampleCaptcha = !empty($matches) ? $matches[1] : '';
    echo "BDC_SP_exampleCaptcha Token: $BDC_SP_exampleCaptcha\n";

    preg_match('/id="BDC_Hs_exampleCaptcha" name="BDC_Hs_exampleCaptcha" value="([a-f0-9]+)"/', $homeHtml, $matches);
    $BDC_Hs_exampleCaptcha = !empty($matches) ? $matches[1] : '';
    echo "BDC_Hs_exampleCaptcha Token: $BDC_Hs_exampleCaptcha\n";

    // Extract cookies
    $cookies = $client->getConfig('cookies')->toArray();
    $sessionId = $cookies['JSESSIONID'];
    $lbSticky = $cookies['LB_STICKY'];

    // Prepare POST payload
    $postPayload = [
        'criteria.crNumber' => '',
        'criteria.companyName' => 'aaa',
        '_eventId__search' => '',
        'BDC_VCID_exampleCaptcha' => $captchaToken,
        'BDC_BackWorkaround_exampleCaptcha' => '1',
        'BDC_Hs_exampleCaptcha' => $BDC_Hs_exampleCaptcha,
        'BDC_SP_exampleCaptcha' => $BDC_SP_exampleCaptcha,
        'captchaCode' => strtoupper($captchaValue),
    ];

    // Set headers with extracted cookies
    $postHeaders = [
        'Cookie' => "JSESSIONID=$sessionId;pll_language=en; lastSavedDir=ltr; LB_STICKY=$lbSticky;",
    ];

    // Make a POST request with the payload and headers
    $postResponse = $client->post("https://www.business.gov.om/portal/searchEstablishments?execution=e1s1", [
        'headers' => $postHeaders,
        'form_params' => $postPayload,
    ]);

    echo $postResponse->getBody();

    // Optional: Follow-up GET request
    $getResponse = $client->get("https://www.business.gov.om/portal/searchEstablishments?execution=e1s2", [
        'headers' => $postHeaders,
    ]);

    echo $getResponse->getBody();

    file_put_contents('output.html', $homeResponse);
    echo 'Response saved to output.html'

} catch (RequestException $e) {
    echo "Error: " . $e->getMessage();
}

?>
