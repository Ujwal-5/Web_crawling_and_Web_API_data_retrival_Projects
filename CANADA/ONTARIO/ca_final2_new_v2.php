<?php
include("Browser_ON.class.php");
$mysql_hostname = "localhost";  
$mysql_user = "root";                 //your mysql user name
$mysql_password = "";                //your mysql password
$mysql_database = "crawler_db";     //your mysql database

$conn = mysqli_connect($mysql_hostname, $mysql_user, $mysql_password,$mysql_database) or die("Opps some thing went wrong");
$res = mysqli_query( $conn,"CALL PROCEDURE_KEYWORDS_3_ontario(@p0,@p1);");
$res = mysqli_query( $conn,'SELECT @p0,@p1');
$data=mysqli_fetch_array($res); 

$objbrowser=new Browser();
//echo $keyword='AAA';
//echo $keyword=$data['@p1'];
echo $keyword=$data['@p1'];
$getValidSessionQuery = mysqli_query( $conn,"select * from Ontario_cookies where status=0 order by SLNO DESC limit 1 ");
$resultGetValidSessionQuery=mysqli_fetch_array($getValidSessionQuery); 
$cokkiesVal=$resultGetValidSessionQuery['Cookie']; 
$SLNO = $resultGetValidSessionQuery['SLNO'];
$url="https://www.appmybizaccount.gov.on.ca/onbis/master/entry.pub?applicationCode=onbis-master&businessService=registerItemSearch";
//$cokkiesVal='dtCookie=v_4_srv_16_sn_537FC70523CB2BBDB9115C21B593A1F7_perc_100000_ol_0_mul_1_app-3A2818f6cf1dba0210_1; x-catalyst-session-global=d5096cd6c79cda86f06ec82815faa9cbce3183fc6038d474451a005c80c9b5e8a3fa80fda41a422f; x-catalyst-timezone=America/Toronto; JSESSIONID=0000HtLu7ZI6Xb2D99jgi61np_1:1egistsvo; rxVisitor=1694601794098UL9CJ0BIPQAEBP9RFT231TR9RR6R3ELD; dtPC=16$214891048_959h-vSRGUHHKCQHUKASFEPDRWELWFDSKNSHRF-0e0; rxvt=1694616691520|1694612516351; dtSa=-; QueueITAccepted-SDFrts345E-V3_onbis=EventId%3Donbis%26QueueId%3Dafd95d59-65e3-4b29-a5ed-2a744985e035%26RedirectType%3Dsafetynet%26IssueTime%3D1694614890%26Hash%3De28f3e9f50ff16886707c0241c47e84776dcbded56df59f61b2f951074e39e1e; x-catalyst-secured-session-onbis-master=1312f310-4d09-48fc-ae34-bece07f9e50b';
$xmldata = $objbrowser->fetchURL1($url,'GET','',$cokkiesVal);
//die();
$va=$objbrowser->getResponce($xmldata);
$arr =$objbrowser->getForms();
echo "<pre>";
print_r($arr);
print_r( $va);


//exit();

$pos=strpos( $xmldata,"viewInstanceKey:");
$pos1=strpos( $xmldata,",callbackNodeParam:'_CBNODE_'");
$pos=$pos+strlen("viewInstanceKey:");
$r=$pos1-$pos;
echo "<br>CBNODE=".$rest = trim(substr($xmldata,$pos+1, $r)," ,'");

$fpos=strpos( $xmldata,"guid:");
$fpos=$fpos+strlen("guid:");

$fpos1=strpos( $xmldata,",asyncInProgress:false");
$fr=$fpos1-$fpos;
echo "<br>CBNODE1=". $frest = trim(substr($xmldata,$fpos, $fr)," ,'");

$serch='<button class="appButton registerItemSearch-tabs-criteriaAndButtons-buttonPad-search appButtonPrimary appSearchButton appSubmitButton appPrimaryButton appNotReadOnly appIndex2" id="';
$spos=strpos( $xmldata,$serch);
$spos1=strpos( $xmldata,'href="#"',$spos);
$spos=$spos+strlen($serch);
$sr=$spos1-$spos;
echo "<br>CBNODE2=". $srest = trim(substr($xmldata,$spos,$sr),'node "');

$cpos=strpos( $xmldata,'containerNodeId',$spos);
$cpos1=strpos( $xmldata,'success:',$cpos);
$cpos=$cpos+strlen('containerNodeId');
$cr=$cpos1-$cpos;

echo "<br>CBNODE5=".$crest = trim(substr($xmldata,$cpos,$cr),"'  ,:");
$apos=strpos( $xmldata,'<input type="hidden" id="node');
$apos1=strpos( $xmldata,'Advanced',$apos);
$apos=$apos+strlen('<input type="hidden" id="node');
$ar=$apos1-$apos;

echo "<br>CBNODE3=". $arest = trim(substr($xmldata,$apos,$ar),"'  ,-:");

$cookie=strpos( $xmldata,"'x-catalyst-session-global':");
$cookie=$cookie+strlen("'x-catalyst-session-global':");
$cookie1=strpos( $xmldata,"x-catalyst-async':true");
$cookieglobalval=$cookie1-$cookie;
$cookieval = trim(substr($xmldata,$cookie, $cookieglobalval)," ,'");
  $Cookieval=array();
  $Cookieval[]="x-catalyst-session-global=".$cookieval."; x-catalyst-timezone=Asia/Phnom_Penh";
echo "<br>CBNODE4=".   $finalcok=implode(';',$Cookieval);

//$resurl = str_ireplace('update.html', 'view.html', $arr[1]['action']);

//$objbrowser->fetchURL($resurl);

$sserch='<input type="hidden" id="node';
$spos=strpos( $xmldata,$sserch);
$spos1=strpos( $xmldata,'-Advanced" name="node',$spos);
$spos=$spos+strlen($sserch);
$sr=$spos1-$spos;
echo "<br> move4=".$ssrest = trim(substr($xmldata,$spos,$sr),'-Advanced" name="node');

$vickyrest= $rest;
/*
QueryString	"abc"
nodeW915-Advanced	"Y"
SourceAppCode	"onbis-corporations"
EntitySubTypeCode	""
nodeW939-ExactSearchYn	""
Status	""
RegistrationDate	""
nodeW934-searchOp	"DayEq"
_scrollTop	"2351.5"
_CBNODE_	"W1254"
_CBNAME_	"invokeMenuCb"
_CBVALUE_	""
_VIKEY_	"0c5b4a29x9374x4f40x8c7bx535208c4faba"
*/


$objbrowser->setFormVar($arr[0]['name'],'QueryString',$keyword);
$objbrowser->setFormVar($arr[0]['name'],'node'.$arest.'-Advanced','Y');
$objbrowser->setFormVar($arr[0]['name'],'SourceAppCode',"onbis-corporations");
$objbrowser->setFormVar($arr[0]['name'],'EntitySubTypeCode','');
$objbrowser->setFormVar($arr[0]['name'],'node'.$arest.'-searchOp','DayEq');
$objbrowser->setFormVar($arr[0]['name'],'_CBASYNCUPDATE_','true');
$objbrowser->setFormVar($arr[0]['name'],'_CBHTMLFRAGNODEID_',$crest);
$objbrowser->setFormVar($arr[0]['name'],'_CBHTMLFRAGID_',$frest);
$objbrowser->setFormVar($arr[0]['name'],'_CBHTMLFRAG_','true');
$objbrowser->setFormVar($arr[0]['name'],'_CBNODE_',$srest);
$objbrowser->setFormVar($arr[0]['name'],'_VIKEY_',$rest);
$objbrowser->setFormVar($arr[0]['name'],'_CBNAME_','buttonPush');

$objbrowser->setFormAction($arr[0]['name'], $arr[0]['action']);

echo $finalData =$objbrowser->submitForm($arr[0]['name'],"POST",$finalcok);



$s2erch='Page size</label><select id="node';
echo "<br>spas=". $spos=strpos( $finalData,$s2erch);
echo "<br>spos1=".$spos1=strpos( $finalData,'PageSize" aria-labelledby="node',$spos);
echo "<br>spas=".$spos=$spos+strlen($s2erch);
echo "<br>SR=".$sr=$spos1-$spos;
echo "<br>s2rest=".$s2rest = trim(substr($finalData,$spos,$sr),'PageSize" aria-labelledby="node');


echo "<br> get data".$xmldata = $objbrowser->fetchURL1($arr[0]['action'],'GET',null,$finalcok);
$objbrowser->setFormVar($arr[0]['name'],'QueryString',$keyword);
$objbrowser->setFormVar($arr[0]['name'],'node'.$arest.'-Advanced','N');
$objbrowser->setFormVar($arr[0]['name'],'_CBNODE_',$s2rest);
$objbrowser->setFormVar($arr[0]['name'],'_CBNAME_','pageSizeChange');
$objbrowser->setFormVar($arr[0]['name'],'_CBVALUE_','4');


echo "submit data". $finalData =$objbrowser->submitForm($arr[0]['name'],"POST",$finalcok);
$arr =$objbrowser->getForms();
echo "<pre> after array";
print_r($arr);
//exit();
$finalData = $objbrowser->fetchURL1($arr[0]['action'],'GET',null,$finalcok);


	file_put_contents("C:/Scripts/XSCAONREG/abc2.html",$finalData);	

 $xpathQuery =array(
    'detail_id'=>'//a[@class="registerItemSearch-results-page-line-ItemBox-resultLeft-viewMenu appMenu appMenuItem appMenuDepth0 appItemSearchResult noSave viewInstanceUpdateStackPush appReadOnly appIndex0"][1]/@id'
    );
    
    
 $detailxpath=  readXpath($finalData,$xpathQuery); 
 
 for($de=0;$de<count($detailxpath['detail_id']);$de++)
 {
 $xpathQuery =array(
    'previousName'=>"//a[@id='".$detailxpath['detail_id'][$de]."']/following::div[@class='appMinimalBox previousNameSearchResult'][1]//span[2]"
    );
     $detail1=  readXpath($finalData,$xpathQuery); 
     print_r($detail1);
     $detailxpath['previousName'][$de]=$detail1['previousName'];
 
 }
 
 echo "<pre>";
 print_r($detailxpath);
  if (count($detailxpath)>=1){
  	$getValidSessionQuery = mysqli_query( $conn,"update Ontario_cookies set status = 1 where SLNO = $SLNO ");
$resultGetValidSessionQuery=mysqli_fetch_array($getValidSessionQuery); 
}
else
{
	$SetKeyworld = mysqli_query( $conn,"update KEYWORDS_3_ontario set FLAG = 11 where KEYWORD = '".$keyword."'");
	$resultSetKeyworld=mysqli_fetch_array($SetKeyworld);
}  	
 print_r($arr);
 for($comp=0;$comp<count($detailxpath['detail_id']);$comp++)
 {
 
 	$cbnode=trim($detailxpath['detail_id'][$comp],'node');
	$objbrowser->setFormVar($arr[0]['name'],'QueryString',$keyword);
	$objbrowser->setFormVar($arr[0]['name'],'node'.$arest.'-Advanced','N');
	$objbrowser->setFormVar($arr[0]['name'],'_CBNAME_','invokeMenuCb');
	$objbrowser->setFormVar($arr[0]['name'],'_CBNODE_',$cbnode);
	$objbrowser->setFormVar($arr[0]['name'],'_VIKEY_',$rest);

	$objbrowser->setFormAction($arr[0]['name'], $arr[0]['action']);
	echo "<br>pagw wise result";
	  $CompanyData =$objbrowser->submitForm($arr[0]['name'],"POST",$finalcok);
	echo "neeeeee submitttt";
$arr2 = $objbrowser->getForms();
      	
	print_r( $arr2 );
	

	$secXpathArr = readXpath($CompanyData,array(
        'section'=>"//ul[@class[contains(.,'appTab')]]/li/a",
        'sectiontab'=>"//ul[@class[contains(.,'appTab')]]/li/a/@id",
        'fullname'=>"//div[@class[contains(.,'appSingleLine appSingleLineNonBlank')]]/descendant::div[@class='appAttrValue']/text()"
      ));
      	echo "<br> printttttttttttttttttttttttttt";
      	echo "<pre>";
	print_r($secXpathArr);
	
	$xpath=Array();
	$xpath['regid']='//span[contains(.,"Corporation Number") or contains(.,"Identification Number")]/following::div[1]/text()';
	$xpath['type']='//span[contains(.,"Type")]/following::div[1]/text()';
	$companyArr=  readXpath($CompanyData,$xpath); 
	print_r($companyArr);
      	for($tab=1;$tab<count($secXpathArr['section']);$tab++)
	{
		echo "<br> second tab is there ";
        $xmldata1=$CompanyData;
		$fpos=strpos( $xmldata1,"guid:");
		$fpos=$fpos+strlen("guid:");
		$fpos1=strpos( $xmldata1,",asyncInProgress:false");
		$fr=$fpos1-$fpos;
		echo "<br> freeeee==". $frest = trim(substr($xmldata1,$fpos, $fr)," ,'");

		$serch="if (catHtmlFragmentCallback('";
		$spos=strpos( $xmldata1,$serch);
		$spos1=strpos( $xmldata1,"','tabSelect',0,{asyncUpdate:",$spos);
		$spos=$spos+strlen($serch);
		$sr=$spos1-$spos;
		echo "<br> srest==". $srest = trim(substr($xmldata1,$spos,$sr),"if (catHtmlFragmentCallback('");

		$pos=strpos( $xmldata1,"viewInstanceKey:");
		$pos1=strpos( $xmldata1,",callbackNodeParam:'_CBNODE_'");
		$pos=$pos+strlen("viewInstanceKey:");
		$r=$pos1-$pos;
		echo "<br> restt==". $rest = trim(substr($xmldata1,$pos+1, $r)," ,'");

		$objbrowser->fetchURL1($arr[0]['action'],'GET',null,$finalcok);
		$objbrowser->setFormVar($arr2[0]['name'],'_CBASYNCUPDATE_',true);
		$objbrowser->setFormVar($arr2[0]['name'],'_CBHTMLFRAGID_',$frest);
		$objbrowser->setFormVar($arr2[0]['name'],'_CBHTMLFRAG_',true);
		$objbrowser->setFormVar($arr2[0]['name'],'_CBNODE_',$srest);
		$objbrowser->setFormVar($arr2[0]['name'],'_VIKEY_',$rest);
		$objbrowser->setFormVar($arr2[0]['name'],'_CBNAME_','tabSelect');
		$objbrowser->setFormVar($arr2[0]['name'],'_CBVALUE_',($tab+1));

		$objbrowser->setFormAction($arr2[0]['name'], $arr2[0]['action']);
		echo "<br>data printttttttttt";
		echo  $xmld = $objbrowser->submitForm($arr2[0]['name'],"POST",$finalcok);
		$CompanyData =$CompanyData.$xmld;
		
		
	}
	if($detailxpath['previousName'][$comp][0] !='')
	{
	    //for($pre=0;$pre<count())
	    echo $previousName="<html>";
	    for($prev=0;$prev<count($detailxpath['previousName'][$comp]);$prev++){
		echo $previousName.="<div class='previousname'>".$detailxpath['previousName'][$comp][$prev]."</div>";

		}
		echo $previousName.="</html>";
		$CompanyData =$CompanyData.$previousName;
	}	
	$type=str_ireplace(" ","_",$companyArr['type'][0]);

	//  check regid is exist or not in table 
    $filename= $companyArr['regid'][0]."_".$type;
	echo $selsql	='select URL from Ontario_REGNO where url="'.$filename.'"';
	$resREG = mysqli_query( $conn,$selsql);
	echo $regCheckArr=mysqli_fetch_array($resREG);
	print_r ($regCheckArr);
	if($regCheckArr['URL']=='')
	{
		$filename= $companyArr['regid'][0]."_".$type;

		$f = file_put_contents("C:/Scripts/XSCAONREG/html/".$filename.'.html',$CompanyData);
		if($f){
			$inssql	='INSERT IGNORE INTO `Ontario_REGNO` (URL) VALUES ("'.$filename.'")';
			$insREG = mysqli_query( $conn,$inssql);
		}	
	}	
	//exit();
hiturl();
}

 
/* 
 QueryString	"ABC"
nodeW560-Advanced	"N"
_scrollTop	"807"
_CBNODE_	"W641"
_CBNAME_	"invokeMenuCb"
_CBVALUE_	""
_VIKEY_	"f8a2bfb5xf270x4ad4x9985xd944d1ef1fa9" */

function hiturl()
{
	$url = "http://54.246.35.195/DEV2.0/Configrator/monitor.php?Browser=Terminal&Service=ontario2_crawling&Machine_Name=SPIDER9";
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
    
function readXpath($html,$xpathArr)
{
    try{
    $mydom=new DOMDocument('1.0','UTF-8');
    //@$mydom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8'));
    @$mydom->loadHTML($html);
    $mydom->encoding = 'UTF-8';
    @$myXpath=new DOMXPath($mydom);
    $keyXpathArr=array_keys($xpathArr);
    $values=array();
    for($xpath=0;$xpath<count($keyXpathArr);$xpath++)
    {
     echo "<br>". $xpathQuery=$xpathArr[$keyXpathArr[$xpath]];
      $xResult=$myXpath->query($xpathQuery);
      echo "<br> length = ".$xResult->length;
      if($xResult->length != 0)
      {
        foreach($xResult as $result)
        {
	      if(trim($result->textContent) !='')
              $values[$keyXpathArr[$xpath]][]=trim(str_replace("\xc2\xa0","",$result->textContent));
           //   else 
            //  $values[$keyXpathArr[$xpath]][]='';
              
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

function readXpath1($html,$xpathArr)
{
    $keyXpathArr=array_keys($xpathArr);
    $valuesdata=array();
    for($xpath=0;$xpath<count($keyXpathArr);$xpath++)
    {
     	$xpathQuery=$xpathArr[$keyXpathArr[$xpath]];
     	$xpathdArr=explode('[*]',$xpathQuery);
	//print_r($xpathArr);
	$temXpathArr=array();
	$tempXpathArr['id']=$xpathdArr[0];
	$value=readXpath($html,$tempXpathArr);
	//print_r($value);
	for($count=0;$count<=count($value['id']);$count++)
	{
		$xpathQuery1=str_ireplace('[*]','['.$count.']',$xpathQuery);
		$tempXpathArr['id']=$xpathQuery1;
		$data=array();
		$data=readXpath($html,$tempXpathArr);
		print_r($data);
		$valuesdata[$keyXpathArr[$xpath]][]=$data['id'][0];
	}

    }
	//echo "<pre>";
	//print_r($valuesdata); 
	return $valuesdata;
}

mysqli_close($conn);



?>
