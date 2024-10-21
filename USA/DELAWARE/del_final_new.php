<?php
$conn = mysqli_connect("localhost", "root", "","crawler_db") or die("Opps some thing  went wrong");
$res = mysqli_query( $conn,"CALL PROCEDURE_KEYWRDS4_DELAWARE(@p0,@p1);");
$res = mysqli_query( $conn,'SELECT @p0,@p1');
$dbCateArr=mysqli_fetch_array($res);
  echo  $dataJsonData =$dbCateArr['@p1'];
$loopData=0;
hiturl();
try {
	//echo $datajson=file_get_contents("http://54.246.35.195/DEV2.0/Configrator/Procedure_Dalaware.php?action=GET");
	//$dataJsonData=json_decode($datajson,'true');
	//print_r($dataJsonData);
	$url="https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx";
	  $html=processCurlRequest($url,$action='GET');
	  $xpathArr['FormAction']="//form/@action";
	  $xpathArr['states']="//input[@id='__VIEWSTATE']/@value";
	  $xpathArr['stategenrator']="//input[@id='__VIEWSTATEGENERATOR']/@value";
	  $xpathArr['validated']="//input[@id='__EVENTVALIDATION']/@value";
	  $xpathArr['name']="//input/@name";
	  $xpathArr['allinput']="//input/@value";
	  $dataexpathArr1=readXpath($html,$xpathArr);
	  echo "<pre>";
	  print_r($dataexpathArr);
	  $postArray=array();
	  $postArray['__EVENTTARGET']='';
	  $postArray['__EVENTARGUMENT']='';
	  $postArray['__VIEWSTATE']=($dataexpathArr1['states'][0]);
	  $postArray['ctl00$ContentPlaceHolder1$frmEntityName']='';
	  $postArray['__VIEWSTATEGENERATOR']=$dataexpathArr1['stategenrator'][1];
	  $postArray['ctl00$ContentPlaceHolder1$frmFileNumber']=$dataJsonData;
	  $postArray['ctl00$ContentPlaceHolder1$hdnPostBackSource']='';
	  $postArray['ctl00$ContentPlaceHolder1$lblMessage'] ='';
	  $postArray['ctl00$ContentPlaceHolder1$btnSubmit']='Search';
	    print_r( $postArray);
	  $mainpost= http_build_query($postArray);
	echo $dataHtml=processCurlRequest($url,$action='POST',$mainpost,$cnt='');
	   
	   if(stristr($dataHtml,"Please complete the reCAPTCHA") !==false)
	   {
	   	echo "calll captchaaaaaa";

	   	//Please complete the reCAPTCHA
		echo $html=getCaptchReponce();
		 $dataexpathArr1=readXpath($html,$xpathArr);
		  echo "<pre>";
		  print_r($dataexpathArr);
		  $postArray=array();
		  $postArray['__EVENTTARGET']='';
		  $postArray['__EVENTARGUMENT']='';
		  $postArray['__VIEWSTATE']=($dataexpathArr1['states'][0]);
		  $postArray['ctl00$ContentPlaceHolder1$frmEntityName']='';
		  $postArray['__VIEWSTATEGENERATOR']=$dataexpathArr1['stategenrator'][1];
		  $postArray['ctl00$ContentPlaceHolder1$frmFileNumber']=$dataJsonData;
		  $postArray['ctl00$ContentPlaceHolder1$hdnPostBackSource']='';
		  $postArray['ctl00$ContentPlaceHolder1$lblMessage'] ='';
		  $postArray['ctl00$ContentPlaceHolder1$btnSubmit']='Search';
		  print_r( $postArray);
		  $mainpost= http_build_query($postArray);
		  echo $dataHtml=processCurlRequest($url,$action='POST',$mainpost,$cnt='');
		   
		   if(stristr($dataHtml,"Please complete the reCAPTCHA") !==false)
		   {
		     echo "I am not able to solve";
	   		exit();
		   }
	       
	   }

		$dataexpathArr=readXpath($dataHtml,$xpathArr);
		  echo "<pre>";
		  print_r($dataexpathArr);
		  
		  $inputArr=array();
		  $inputArr['id']='//a[@onclick="return validateStatus(this);"]/@href';
		  $inputArr['idkey']='//span[contains(@id, "lblFileNumber")]';
		  $inputXpathArr=readXpath($dataHtml,$inputArr);
		  echo "<pre>";
		  print_r($inputXpathArr);
		  
	
	  

	    if (!array_key_exists("idkey",$inputXpathArr))
		{
		 	      file_get_contents('http://54.246.35.195/DEV2.0/Configrator/Procedure_Dalaware.php?action=UPDATE&id='.$dataJsonData['id']);
		 	     // continue;
		 	      exit();
		}
	  for($dela=0;$dela<count($inputXpathArr['idkey']);$dela++)
	  {
	    $finalhtml='';
	    $passName=str_ireplace('javascript:__doPostBack(','',$inputXpathArr['id'][$dela]);
	    echo $passName=trim($passName,"',)");
	    $postArray=array();
	    $postArray['__EVENTTARGET']=$passName;
	    $postArray['__EVENTARGUMENT']='';
	    $postArray['__VIEWSTATE']=($dataexpathArr['states'][0]);
	    $postArray['ctl00$ContentPlaceHolder1$frmEntityName']=$dataJsonData;
	    $postArray['__VIEWSTATEGENERATOR']=$dataexpathArr['stategenrator'][1];
	    $postArray['ctl00$ContentPlaceHolder1$frmFileNumber']='';
	    $postArray['ctl00$ContentPlaceHolder1$hdnPostBackSource']='';
	    $postArray['ctl00$ContentPlaceHolder1$lblMessage'] ='';
	   // $postArray['ctl00$ContentPlaceHolder1$btnSubmit']='Search';
	     print_r( $postArray);
	    $mainpost= http_build_query($postArray);
	    echo $finalhtml=processCurlRequest($url,$action='POST',$mainpost,$cnt='');
	     $mainXpathArr=array();
	    $mainXpathArr['fileName']='//span[@id="ctl00_ContentPlaceHolder1_lblFileNumber"]';
	    $mainDataArr=readXpath($finalhtml,$mainXpathArr);
	    echo "<pre> mian html";
	    print_r($mainDataArr['fileName']);
	    if($mainDataArr['fileName'][0])
	    {
	    	file_put_contents("C:/wamp64/www/script_php/XSUSREG/del/dela_html/".$mainDataArr['fileName'][0].'.html',$finalhtml);
	    	echo"<br>".$update = "UPDATE `TEMP_URL_DELAWARE` SET `STATUS` =10  WHERE company_number = '".$dataJsonData."'";
			mysqli_query($conn,$update) OR DIE('WRONG UPDATE 3');
	    	storeDataS3($finalhtml,$mainDataArr['fileName'][0]);
	    }	
	    //exit();
	    if($dela <=0)
	     {
	         echo "updateeeee";
	          file_get_contents('http://54.246.35.195/DEV2.0/Configrator/Procedure_Dalaware.php?action=UPDATE&id='.$dataJsonData['id']);
	     }
	  }
  
	  } 
	catch (Exception $e) {
		// Handle the exception
		echo 'Caught exception: ' . $e->getMessage() . "\n";
	    }
  

function readXpath($html,$xpathArr)
{
    try{ 
    $mydom=new DOMDocument('1.0','UTF-8');
    //@$mydom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8'));
    $mydom->loadHTML($html);
    $mydom->encoding = 'UTF-8';
    @$myXpath=new DOMXPath($mydom);
    $keyXpathArr=array_keys($xpathArr);
    $values=array();
    for($xpath=0;$xpath<count($keyXpathArr);$xpath++)
    {
      $xpathQuery=$xpathArr[$keyXpathArr[$xpath]];
      $xResult=$myXpath->query($xpathQuery);
      if($xResult->length != 0)
      {
        foreach($xResult as $result)
        {
              $values[$keyXpathArr[$xpath]][]=trim(str_replace("\xc2\xa0","",$result->textContent));
        }
      }
      //else
       //$values[$keyXpathArr[$xpath]][]=array();
   }
      return $values;
    }catch(Exception $e)
     {
            echo"ERROR in(readXpath):".$e->getMessage();
     }
}

 function processCurlRequest($url,$action='GET',$post='',$cnt='')
  {
   
    $ch = curl_init();

      // sleep(rand(1,5));
      curl_setopt($ch, CURLOPT_URL,$url);
      curl_setopt($ch, CURLOPT_HEADER, true);
      curl_setopt($ch, CURLOPT_COOKIEJAR, "delcookie.txt");
      curl_setopt($ch, CURLOPT_COOKIEFILE, "delcookie.txt");
     curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
      curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
      curl_setopt($ch, CURLOPT_TIMEOUT, 0);
      curl_setopt($ch, CURLOPT_AUTOREFERER, 1);
      curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);

      if($action!=='GET'){
      curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $action);
      curl_setopt($ch, CURLOPT_POSTFIELDS,$post);
      }else{
      curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
      }
	/*curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*//*;q=0.8',
    'Host: www.registreentreprises.gouv.qc.ca',
    'Origin: https://www.registreentreprises.gouv.qc.ca','Content-Length: 0']); */
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*//*;q=0.8',
    'Accept-Language: en-US,en;q=0.5',
    'Content-Type: application/x-www-form-urlencoded',
    'Origin: https://icis.corp.delaware.gov',
    'Connection: keep-alive',
    'Referer: https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx',
    'Upgrade-Insecure-Requests: 1',
    'Sec-Fetch-Dest: document',
    'Sec-Fetch-Mode: navigate',
    'Sec-Fetch-Site: same-origin',
    'Sec-Fetch-User: ?1',
]);

//   $agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36";
      //curl_setopt($ch, CURLOPT_USERAGENT,$agent);
//       curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 1);
// curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 1);
      curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($ch, CURLOPT_REFERER, "https://example.com/aboutme.html");

   $response= curl_exec($ch);
      curl_close($ch);
      file_put_contents('response.html',$response);


    return $response;

  }
  
 function solveRecaptcha($apiKey, $siteKey, $url) {
    try {
        // Submitting the CAPTCHA to 2captcha for solving
        $ch = curl_init('http://2captcha.com/in.php');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query([
            'key' => $apiKey,
            'method' => 'userrecaptcha',
            'googlekey' => $siteKey,
            'pageurl' => $url,
            'json'=> 1,
        ]));
        
        

        
        $response = curl_exec($ch);
        curl_close($ch);
                 print_r($response);

        $responseArray = json_decode($response, true);

        if ($responseArray['status'] != 1) {
            throw new Exception('Failed to get captcha ID from 2captcha');
        }

        $captchaId = $responseArray['request'];

        // Polling 2captcha for the solution
        for ($i = 0; $i < 30; $i++) { // Adjust the number of attempts as needed
            $ch = curl_init("http://2captcha.com/res.php?key={$apiKey}&action=get&id={$captchaId}&json=1");
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $solutionResponse = curl_exec($ch);
            curl_close($ch);

            $solutionResponseArray = json_decode($solutionResponse, true);

            if ($solutionResponseArray['status'] == 1) {
                return $solutionResponseArray['request'];
            }

            sleep(5);
        }

        throw new Exception('Failed to get captcha solution from 2captcha');
    } catch (Exception $e) {
        // Handle the exception, e.g., log the error or display a user-friendly message
        echo 'Caught exception: ',  $e->getMessage(), "\n";
    }
}

 function getCaptchReponce()
 {
 
 
 	// Replace with your 2captcha API key
	$apiKey = 'your_2captcha_key';

	// Replace with the actual reCAPTCHA site key and URL
	$siteKey = '6Le1dNQZAAAAAGYNA9djIXojESuOKtvMLtRoga3r';
	$url = 'https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx';

	// Solve the reCAPTCHA
	$captchaSolution = solveRecaptcha($apiKey, $siteKey, $url);

	// Use captchaSolution in your automation process (e.g., filling out a form)
	echo "Captcha solution: $captchaSolution\n";


	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, 'https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx');
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
	curl_setopt($ch, CURLOPT_HTTPHEADER, [
	    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8',
	    'Cache-Control: max-age=0',
	    'Connection: keep-alive',
	    'Content-Type: application/x-www-form-urlencoded',
	    'Origin: https://icis.corp.delaware.gov',
	    'Referer: https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx',
	    'Sec-Fetch-Dest: document',
	    'Sec-Fetch-Mode: navigate',
	    'Sec-Fetch-Site: same-origin',
	    'Sec-Fetch-User: ?1',
	    'Upgrade-Insecure-Requests: 1',
	    'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
	    'sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
	    'sec-ch-ua-mobile: ?0',
	    'sec-ch-ua-platform: "Linux"',
	    'Accept-Encoding: gzip',
	]);
	//curl_setopt($ch, CURLOPT_COOKIE, 'ASP.NET_SessionId=xndikg455yza5q55bomaiezx; TS01877c38=01d343b75f90a59311a4973ed944ba7da544559f60378b5d10f7fdbe9d8f226c176d2d88bc28798773b98bbecfcbbe4103d6d04e61');
	curl_setopt($ch, CURLOPT_POSTFIELDS, 'g-recaptcha-response='.$captchaSolution);

	 $response = curl_exec($ch);

	curl_close($ch);
	return $response;
 
 }
  	function hiturl()
{
	$url = "http://3.254.232.204/DEV2.0/Configrator/monitor.php?Browser=Terminal&Service=DEL_US&Machine_Name=SAKSHI_MACHINE";
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_HEADER, 1);
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); //0 false for get info of file [catch output] 
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
	curl_setopt($ch, CURLOPT_TIMEOUT, 100);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 150);

	$response = curl_exec($ch);
	print_r($response);
}
  function storeDataS3($content,$cId)
  {
  
  
  		$data = array(
	    'HTML' => $content,
	    'NAME' => $cId,
	    'USER_ID' => 'sakshi'
	);

	$json_data = json_encode($data);

	try {
	    echo 'datattatatta';
	    $url = 'http://18.201.184.118/xsusreg-delaware-data-configure_api/DEConfigureS3.php';

	    $ch = curl_init($url);

	    // Set cURL options
	    curl_setopt($ch, CURLOPT_POST, 1);
	    curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
	    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
	    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	    // Execute cURL session
	  echo  $response = curl_exec($ch);

	    // Check for cURL errors
	    if (curl_errno($ch)) {
		echo 'Curl error: ' . curl_error($ch);
	    }

	    // Close cURL session
	    curl_close($ch);

	    // You can print the response if needed
	    // echo $response;
	} catch (Exception $e) {
	    // Handle exception
	    echo 'Error: ' . $e->getMessage();
	}
  }
  

?>




