<?php
ini_set('max_execution_time', 0);
print_r("Hello");

$a= new XSUSREGHO();
$a->startProcess('county');



Class XSUSREGHO {
/**
 * Create a new instance.
 *
 * @return void
 */
public $input_folder_html_name;
public $input_folder_done_name;
public $input_folder_skip_name;
public $input_folder_json_name;
public $input_file_extention;
public $output_file_extention;
function __construct()
  {
      /*****input folder*****/
      $this->input_folder_html_name = 'html';
      /*****output folder*****/
      //move .html file if done
      $this->input_folder_done_name = 'done';
      //move .html file if skip
      $this->input_folder_skip_name = 'skip';
      //move .json file if create json using html file
      $this->input_folder_json_name = 'json';
      //input file extention
      $this->input_file_extention = '.html';
      //output file extention
      $this->output_file_extention = '.json';
  }
function startProcess($countyCode){
    $isSuccesCnt = 0;
    $isSkippedCnt = 0;
    $todo_path = __DIR__."/".$countyCode."/".$this->input_folder_html_name."/";
    $done_path = __DIR__."/".$countyCode."/".$this->input_folder_done_name."/";
    if(!is_dir($done_path)) {
      mkdir($done_path, 0777, true);
      chmod($done_path, 0777);
    }
    $skip_path = __DIR__."/".$countyCode."/".$this->input_folder_skip_name."/";
    if(!is_dir($skip_path)) {
      mkdir($skip_path, 0777, true);
      chmod($skip_path, 0777);
    }
    $json_path = __DIR__."/".$countyCode."/".$this->input_folder_json_name."/";
    if(!is_dir($json_path)) {
      mkdir($json_path, 0777, true);
      chmod($json_path, 0777);
    }
    $files = scandir($todo_path);
    /* Hide this */
    $key = 0;
    $hideName = array('.','..','.DS_Store'); 
    foreach ($files as $key1 => $name) {
        if(in_array($name, $hideName)) {
               unset($files[$key1]);
            }
            // if($name==$companyNo)
            //   $key=$key1;
          
      }
    $files = array_values($files);
    
    if(count($files) > 0) {
       foreach ($files as $fileNameKey => $fileName) {
          $todo_file_path = $todo_path.$fileName;
          $done_file_path = $done_path.$fileName;
          $skip_file_path = $skip_path.$fileName;
          if(file_exists($todo_file_path)){
          	 $json_res_arr = $this->jsonByXpath($todo_file_path);
             print_r($json_res_arr);
            //  system("pause");
             if(array_key_exists('FileNumber', $json_res_arr)){
         	     $json_file_path = $json_path.basename($todo_file_path,$this->input_file_extention).$this->output_file_extention;
	             $info = json_encode($json_res_arr,JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE);
	             if($info != '' && $info != null){
	               $file = fopen($json_file_path,'w+') or die("File not found");
	               fwrite($file, $info);
	             }
               if(file_exists($json_file_path)){
                  rename($todo_file_path,$done_file_path);
                  $isSuccesCnt = $isSuccesCnt + 1;
               } else {
                  rename($todo_file_path,$skip_file_path);
                  $isSkippedCnt = $isSkippedCnt + 1;
               }
             } else {
                echo "FileNumber is not present.";
                rename($todo_file_path,$skip_file_path);
                $isSkippedCnt = $isSkippedCnt + 1;
             }
          }
       }
    } else {
      echo "Html File is not found: ".$countyCode."\n";
    }
    echo "SUCCESS COUNT : ".$isSuccesCnt."\n";
    echo "SKIPPED COUNT : ".$isSkippedCnt."\n";
    $result = array("SUCCESS"=>$isSuccesCnt,"SKIPPED"=>$isSkippedCnt);
    return $result;
}
function jsonByXpath($serverFilePath) {
      
	    $xpathArr = $this->setXpathValue();

	    $jsonArr = [];
	    $xPathArr = [];
      $arrayXpathPropertiesArr=[];
	    foreach ($xpathArr as $xpathKey => $xpathValue) {
	      $xPathArr[$xpathKey] = $xpathValue['XPATH'];
        if($xpathValue['IS_MULTIPLE_TYPE'] == '1'){
          $arrayXpathPropertiesArr[]=$xpathKey;
        }
	    }
      echo "<pre>";print_r($arrayXpathPropertiesArr);

	    $fdata = file_get_contents($serverFilePath);
	    $fileNumber = basename($serverFilePath,$this->input_file_extention);
	    $xpathQuery = $this->readXpath($fdata, $xPathArr,$arrayXpathPropertiesArr);
	    //echo "<pre>";print_r($xpathQuery);exit;
	    $jsonArr['FileNumber'] = $fileNumber;
	    foreach ($xpathQuery as $key => $value) {
  	    if ($xpathArr[$key]['TYPE'] == '1') {
  	      $jsonArr[$key] = null;
  	      if(count($value[0]) > 0){
  	        $jsonArr[$key] = $value;
  	      }
  	    } else {
  	      $jsonArr[$key] = null;
  	      if(count($value) > 0){
  	        if(is_array($value[0])){
             if(count($value[0]) > 0){
  	          foreach ($value[0] as $key1 => $val1) {
  	            $tempArr = [];
  	            $isValueExists = false;
  	            foreach ($val1 as $key2 => $val2) {
  	              $tempArr[$key2] = null;
                  if(is_array($val2)){
                    if(count($val2) > 0){
                     $isValueExists = true;
                     $tempArr[$key2] = $val2;
                    }
                  } else {
                    if($val2 != "Â "){
                     $isValueExists = true;
                     $tempArr[$key2] = $val2;
                    }
                  }
  	            }

  	            if(count($tempArr) > 0 && $isValueExists){
  	               $jsonArr[$key][] = $tempArr;
  	             }
  	            }
              }
  	        } else {
  	          $jsonArr[$key] = $value[0];
  	        }

  	      }
  	    }
	  }
	  return $jsonArr;
  }
function readXpath($html, $xpathArr,$multipleDataPropertiesArr=null)
{
  if (!empty($html)) {

  print_r("Taking values from sources html response...\n");

  try {
    $mydom = new DOMDocument('1.0', 'UTF-8');
    @$mydom->loadHTML($html);
    $mydom->encoding = 'UTF-8';
    $myXpath = new DOMXPath($mydom);
    $keyXpathArr = array_keys($xpathArr);
    $values = array();
    for ($xpath = 0; $xpath < count($keyXpathArr); $xpath++) {
      if(in_array($keyXpathArr[$xpath], $multipleDataPropertiesArr)){
        $directorsArr = $this->readXpath1($html, $xpathArr[$keyXpathArr[$xpath]],$multipleDataPropertiesArr);
        $values[$keyXpathArr[$xpath]][] = $directorsArr;
      }else{
      $xpathQuery = $xpathArr[$keyXpathArr[$xpath]];
      $xResult = $myXpath->query($xpathQuery);
      //print_r($xResult);
      if ($xResult->length != 0) {
        foreach ($xResult as $result) {
          $values[$keyXpathArr[$xpath]][] = trim($result->textContent);
        }
      } else {
        $values[$keyXpathArr[$xpath]][] = array();
      }
     }
    }
    //print_r($values);
    return $values;
  } catch (Exception $e) {
    $e->getMessage();
  }
 }
}
function readXpath1($html,$xpathArr,$multipleDataPropertiesArr=null)
{
    print_r($xpathArr);
    $keyXpathArr=array_keys($xpathArr);
    $valuesdata=array();
    for($xpath=0;$xpath<count($keyXpathArr);$xpath++)
    {
      $xpathQuery=$xpathArr[$keyXpathArr[$xpath]];
      $xpathdArr=explode('[*]',$xpathQuery);
      //print_r($xpathArr);
      $temXpathArr=array();
      $tempXpathArr['id']=$xpathdArr[0];
      $value=$this->readXpath($html,$tempXpathArr,$multipleDataPropertiesArr);
      // print_r($xpathdArr);
      for($count=1;$count<=count($value['id']);$count++)
      {
        // print_r($xpathQuery);die;
        $xpathQuery1=str_ireplace('[*]','['.$count.']',$xpathQuery);
        $tempXpathArr['id']=$xpathQuery1;
        $data=$this->readXpath($html,$tempXpathArr,$multipleDataPropertiesArr);
        if (strpos($xpathQuery, 'grid_principalList') !== false) {
          for ($i=0; $i <count($data['id']) ; $i++) { 
            $valuesdata[$keyXpathArr[$xpath]][]=$data['id'][$i];
          }
          // print_r($valuesdata);
          }else{
            $valuesdata[$keyXpathArr[$xpath]][]=$data['id'][0];
          }
      }
    }
  //echo "<pre>";
  print_r($valuesdata);
    $finalArr = array();
    if(count($valuesdata) > 0){
      if(count($keyXpathArr) > 0){
        $totalElement = count($valuesdata[$keyXpathArr[0]]);
        for ($i=0; $i < $totalElement; $i++) { 
          $temArr = array();
          foreach ($keyXpathArr as $key2 => $value3) {
             $temArr[$value3] = $valuesdata[$value3][$i];
        }
        $finalArr[] = $temArr;
      }
    }
    //echo "<pre>";print_r($finalArr);exit;
  }
  if (strpos($xpathQuery, 'grid_principalList') !== false) {
    $farr=array();
    for ($i=0; $i <count($finalArr) ; $i++) {
      if (empty($finalArr[$i]['Title'])) {
        // echo "\n hello \n";
        // print_r($finalArr[$i]);die;
        unset($finalArr[$i]);
      }else{
        $farr[$i]=$finalArr[$i];
      } 
    }
    // print_r($farr);die;
    return $farr;
  }

  return $finalArr;
}
function setXpathValue()
{
     $xpathArr = array();
    
    //  $xpathArr['RegNo'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[2]/td[1]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Business No.' 
    //  );
    //  $xpathArr['Name'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[2]/td[2]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Legal Name' 
    //  );
    //  $xpathArr['Type'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[4]/td[1]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Type' 
    //  );
    //  $xpathArr['Status'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[2]/td[3]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Status' 
    //  );
    //  $xpathArr['OrganizationDate'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[6]/td[2]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Effective Date' 
    //  );
    // $xpathArr['Jurisdiction'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[4]/td[2]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'State of Inc' 
    //  );
    //  $xpathArr['InactiveDate'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[6]/td[1]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Expiring Date' 
    //  );
    //  $xpathArr['ReasonForStatus'] = array( 
    //   'XPATH' => '',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => '' 
    //  );
    
    //In single linePrincipalAddress
    // $xpathArr['PrincipalAddress'] = array( 
    //   'XPATH' => '',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => '' 
    //  );
    // //with AddressLine1, AddressLine2...AddressLineN
    // $xpathArr['PrincipalAddress'] = array(
    //     'XPATH' => array(
    //         'AddressLine1' => '',
    //         'AddressLine2' => '',
    //         'AddressLine3' => ''
    //     ),
    //     'TYPE' => '1',
    //   'IS_MULTIPLE_TYPE' => '1',
    //     'ORIGINAL_FIELD_NAME' => ''
    //   );
    // //with name,address and date
    // $xpathArr['PrincipalAddress'] = array(
    //     'XPATH' => array(
    //         'Name' => '',
    //         'Address' => '',
    //         'Date' => ''
    //     ),
    //     'TYPE' => '1',
    //   'IS_MULTIPLE_TYPE' => '1',
    //     'ORIGINAL_FIELD_NAME' => ''
    //   );
      // with AddressLine1, AddressLine2... City, State, Zip, Country
      $xpathArr['InformaciÃ³n General'] = array(
        'XPATH' => array(
            'Circunscripción Registral' => '//table[@border="1"]//th[contains(text(),"Circunscripción Registral:")]/following-sibling::td/text()',
            'Ubicación de la Empresa' => '//table[@border="1"]//th[contains(text(),"Ubicación de la Empresa:")]/following-sibling::td/text()',
            'Tipo de Comerciante' => '//table[@border="1"]//th[contains(text(),"Tipo de Comerciante:")]/following-sibling::td/text()',
            'Tipo de Capital' => '//table[@border="1"]//th[contains(text(),"Tipo de Capital:")]/following-sibling::td/text()',
            'Razón Social' => '//table[@border="1"]//th[contains(text(),"Razón Social:")]/following-sibling::td/text()',
            'Denominación Social' => '//table[@border="1"]//th[contains(text(),"Denominación Social:")]/following-sibling::td/text()',
            'Nombre Comercial' => '//table[@border="1"]//th[contains(text(),"Nombre Comercial:")]/following-sibling::td/text()',
            'Siglas' => '//table[@border="1"]//th[contains(text(),"Siglas:")]/following-sibling::td/text()',
            'Dirección de la Empresa' => '//table[@border="1"]//th[contains(text(),"Dirección de la Empresa:")]/following-sibling::td/text()',
            'Domicilio' => '//table[@border="1"]//th[contains(text(),"Domicilio:")]/following-sibling::td/text()',
            'Objeto Social de la Empresa' => '//table[@border="1"]//th[contains(text(),"Objeto Social de la Empresa:")]/following-sibling::td/text()',
            'Vigencia' => '//table[@border="1"]//th[contains(text(),"Vigencia:")]/following-sibling::td/text()',
            'Inscrito CCI' => '//table[@border="1"]//th[contains(text(),"Inscrito CCI:")]/following-sibling::td/text()',
            'Finalidad' => '//table[@border="1"]//th[contains(text(),"Finalidad:")]/following-sibling::td/text()',
            'Estado' => '//table[@border="1"]//th[contains(text(),"Estado:")]/following-sibling::td/text()',
            'Observaciones' => '//table[@border="1"]//th[contains(text(),"Observaciones:")]/following-sibling::td/text()',
        ),
        'TYPE' => '0',
        'IS_MULTIPLE_TYPE' => '1',
        'ORIGINAL_FIELD_NAME' => 'InformaciÃ³n General'
    );
    
    $xpathArr['Antecedentes'] = array(
      'XPATH' => array(
          'Tipo Libro' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Tipo Libro")]/ancestor::tr/following-sibling::tr/td[1]',
          'Tomo' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Tomo")]/ancestor::tr/following-sibling::tr/td[2]',
          'Tomo Bis' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Tomo Bis")]/ancestor::tr/following-sibling::tr/td[3]',
          'Libro' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Libro")]/ancestor::tr/following-sibling::tr/td[4]',
          'Libro Bis' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Libro Bis")]/ancestor::tr/following-sibling::tr/td[5]',
          'Inscripción' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Ins")]/ancestor::tr/following-sibling::tr/td[6]',
          'Inscripción Bis' => '//h3[contains(text(), "Antecedentes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Ins. Bis")]/ancestor::tr/following-sibling::tr/td[7]',
      ),
      'TYPE' => '0',
      'IS_MULTIPLE_TYPE' => '1',
      'ORIGINAL_FIELD_NAME' => 'Antecedentes'
  );
  
  
  $xpathArr['Asientos de Presentación'] = array(
    'XPATH' => array(
        'No. Asiento' => '//h3[contains(text(), "Asientos de Presentación")]//following-sibling::table[@border="1"][1]//th[4][contains(text(),"Estado")]/ancestor::tr/following-sibling::tr/td[1]',
        'No. Presentation' => '//h3[contains(text(), "Asientos de Presentación")]//following-sibling::table[@border="1"][1]//th[4][contains(text(),"Estado")]/ancestor::tr/following-sibling::tr/td[2]',
        'Fecha Presentación' => '//h3[contains(text(), "Asientos de Presentación")]//following-sibling::table[@border="1"][1]//th[4][contains(text(),"Estado")]/ancestor::tr/following-sibling::tr/td[3]',
        'Estado' => '//h3[contains(text(), "Asientos de Presentación")]//following-sibling::table[@border="1"][1]//th[4][contains(text(),"Estado")]/ancestor::tr/following-sibling::tr/td[4]',
        'Acto/Contrato' => '//h3[contains(text(), "Asientos de Presentación")]//following-sibling::table[@border="1"][1]//th[4][contains(text(),"Estado")]/ancestor::tr/following-sibling::tr/td[5]',
        'Función Empresa' => '//h3[contains(text(), "Asientos de Presentación")]//following-sibling::table[@border="1"][1]//th[4][contains(text(),"Estado")]/ancestor::tr/following-sibling::tr/td[7]',
        // 'Type' => '(//table[@class="results display"])[9]/tr[*]/td[7]/text()',
        // 'Director' => '(//table[@class="results display"])[9]/tr[*]/td[8]/text()',
    ),
    'TYPE' => '0',
    'IS_MULTIPLE_TYPE' => '1',
    'ORIGINAL_FIELD_NAME' => 'Asientos de Presentación'
);


$xpathArr['Resúmenes'] = array(
  'XPATH' => array(
      'No. Asiento' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"No. Asiento")]/ancestor::tr/following-sibling::tr[*]/td[1]',
      'Inscripción' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Inscripción")]/ancestor::tr/following-sibling::tr[*]/td[2]',
      'No. Presentación' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"No. Presentación")]/ancestor::tr/following-sibling::tr[*]/td[3]',
      'Clasificación' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Clasificación")]/ancestor::tr/following-sibling::tr[*]/td[4]',
      'Transacción' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Transacción")]/ancestor::tr/following-sibling::tr[*]/td[5]',
      'Fecha InscripciÃ³n' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Fecha InscripciÃ³n")]/ancestor::tr/following-sibling::tr[*]/td[7]',
      'Estado' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Estado")]/ancestor::tr/following-sibling::tr[*]/td[8]',
      'Rel' => '//h3[contains(text(), "Resúmenes")]//following-sibling::table[@border="1"][1]//th[contains(text(),"Rel.")]/ancestor::tr/following-sibling::tr[*]/td[9]',
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Resúmenes'
);


$xpathArr['Derechos'] = array(
  'XPATH' => array(
      'No. Asiento' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[1][contains(text(),"No. Asiento")]/ancestor::tr/following-sibling::tr[*]/td[1]/text()',
      'Nombre Completo' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Nombre Completo")]/ancestor::tr/following-sibling::tr[*]/td[2]',
      'Tipo Socio' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Tipo Socio")]/ancestor::tr/following-sibling::tr[*]/td[3]',
      'Capital' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[4][contains(text(),"Capital")]/ancestor::tr/following-sibling::tr[*]/td[4]',
      'Puesto Directivo' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Puesto Directivo")]/ancestor::tr/following-sibling::tr[*]/td[5]',
      'Partes Sociales/Acciones' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Partes Sociales/Acciones")]/ancestor::tr/following-sibling::tr[*]/td[6]',
      'Porcentaje Participación' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Porcentaje Participación")]/ancestor::tr/following-sibling::tr[*]/td[7]',
      'Fecha Constitución' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Fecha Constitución")]/ancestor::tr/following-sibling::tr[*]/td[8]',
      'Fecha Expiración' => '//h3[contains(text(), "Derechos")]//following-sibling::table[@border="1"]//th[contains(text(),"Fecha Expiración")]/ancestor::tr/following-sibling::tr[*]/td[9]',
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Derechos'
);


$xpathArr['Capital'] = array(
  'XPATH' => array(
      'Capital MÃanimo' => '//h3[contains(., "Capital")]/following-sibling::table[2]/tr[*]/td[1]/text()',
      'Capital Maximus' => '//h3[contains(., "Capital")]/following-sibling::table[2]//tr[*]/td[2]/text()',
      'Capital SusCrit' => '//h3[contains(., "Capital")]/following-sibling::table[2]//tr[*]/td[3]/text()',
      'Capital Suscrito' => '//h3[contains(., "Capital")]/following-sibling::table[2]//tr[*]/td[3]/text()',
      'Capital Pagado' => '//h3[contains(., "Capital")]/following-sibling::table[2]//tr[*]/td[4]/text()',
      'Valor Nominal' => '//h3[contains(., "Capital")]/following-sibling::table[2]//tr[*]/td[5]/text()',
      'Historial de Aumentos' =>'//h3[contains(., "Capital")]/following-sibling::table[2]//tr[*]/td[6]/text()',


      // 'Id' => '',
      // 'Status' => ''
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Capital'
);

$xpathArr['Sucursales/Establecimiento Mercantil'] = array(
  'XPATH' => array(
      'CÃ³digo' => '//table[@border="1"]//th[1][contains(text(),"CÃ³digo")]/ancestor::tr/following-sibling::tr[*]/td[1]/text()',
      'Nombre Sucursal' => '//table[@border="1"]//th[2][contains(text(),"Nombre Sucursal")]/ancestor::tr/following-sibling::tr[*]/td[2]/text()',
      'UbicaciÃ³n' => '//table[@border="1"]//th[3][contains(text(),"UbicaciÃ³n")]/ancestor::tr/following-sibling::tr[*]/td[3]/text()',
      'DirecciÃ³n' => '//table[@border="1"]//th[4][contains(text(),"DirecciÃ³n")]/ancestor::tr/following-sibling::tr[*]/td[4]/text()',
      'Encargado' => '//table[@border="1"]//th[5][contains(text(),"Encargado")]/ancestor::tr/following-sibling::tr[*]/td[5]/text()',
      'Capital Sucursal' => '//table[@border="1"]//th[6][contains(text(),"Capital Sucursal")]/ancestor::tr/following-sibling::tr[*]/td[6]/text()',
      'Giro Principal' => '//table[@border="1"]//th[7][contains(text(),"Giro Principal")]/ancestor::tr/following-sibling::tr[*]/td[7]/text()',
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Sucursales/Establecimiento Mercantil'
);


$xpathArr['Representante'] = array(
  'XPATH' => array(
      'No.' => '//h3[contains(text(), "Representante")]//following-sibling::table[@border="1"][1]//th[contains(text(),"No.")]/ancestor::tr/following-sibling::tr[*]/td[1]/text()',
      'Nombre Miembro' => '//table[@border="1"]//th[2][contains(text(),"Nombre Miembro")]/ancestor::tr/following-sibling::tr[*]/td[2]/text()',
      'ObservaciÃ³n' => '//table[@border="1"]//th[3][contains(text(),"ObservaciÃ³n")]/ancestor::tr/following-sibling::tr[*]/td[3]/text()',
      'Puesto Directivo' => '//table[@border="1"]//th[4][contains(text(),"Puesto Directivo")]/ancestor::tr/following-sibling::tr[*]/td[4]/text()',
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Representante'
);


$xpathArr['Poderes'] = array(
  'XPATH' => array(
      'No. Asiento' => '//form/table/tr[*]/td[1]/text()',
      'Nombre Completo' => '//form/table/tr[*]/td[2]/text()',
      'Nombre del Cargo' => '//form/table/tr[*]/td[3]/text()',
      'Fecha ConstituciÃ³n' => '//form/table/tr[*]/td[4]/text()',
      'ObservaciÃ³n' => '//form/table/tr[*]/td[5]/text()',
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Poderes'
);

$xpathArr['Antecedente Poderes'] = array(
  'XPATH' => array(
      'Representante Legal' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[1]/text()",
      'Tipo Libro' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[2]/text()",
      'Tomo' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[3]/text()",
      'Tomo Bis' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[4]/text()",
      'Libro' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[5]/text()",
      'Libro Bis' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[6]/text()",
      'Ins.' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[7]/text()",
      'Ins. Bis' => "//h3[contains(., 'Antecedente Poderes')]/following-sibling::table//tr/following-sibling::tr[*]//tr/following-sibling::tr/td[8]/text()",
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Antecedente Poderes'
);


$xpathArr['Gravámenes'] = array(
  'XPATH' => array(
      'No. de Asiento' => '//h3[contains(., "Gravámenes")]/following-sibling::table[2]/tr[*]/td[1]/text()',
      'Gravamen' => '//h3[contains(., "Gravámenes")]/following-sibling::table[2]/tr[*]/td[2]/text()',
      'A Favor de' => '//h3[contains(., "Gravámenes")]/following-sibling::table[2]/tr[*]/td[3]',
      'Fecha de Constitución' => '//h3[contains(., "Gravámenes")]/following-sibling::table[2]/tr[*]/td[4]/text()',
      'Fecha de Expiración' => '//h3[contains(., "Gravámenes")]/following-sibling::table[2]/tr[*]/td[5]/text()',
      'Rel.' => '//h3[contains(., "Gravámenes")]/following-sibling::table[2]/tr[*]/td[7]/text()'
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Gravámenes'
);

$xpathArr['Restricciones'] = array(
  'XPATH' => array(
    'No. de Asiento' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[1]/text()',
    'Tipo de Restricción' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[2]/text()',
    'Fecha de Inicio' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[4]/text()',
    'Fecha de Fin' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[5]/text()',
    'Plazo' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[6]/text()',
    'Sobre Derechos' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[7]/text()',
    'Observaciones' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[8]/text()',
    'Estado' => '//h3[contains(., "Restricciones")]/following-sibling::table[2]/tr[*]/td[9]/text()',
  ),
  'TYPE' => '0',
  'IS_MULTIPLE_TYPE' => '1',
  'ORIGINAL_FIELD_NAME' => 'Restricciones'
);



  
    // $xpathArr['MailingAddress'] = array( 
    //   'XPATH' => '',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => '' 
    //  );
    // $xpathArr['MailingAddress'] = array(
    //     'XPATH' => array(
    //         'AddressLine1' => '',
    //         'AddressLine2' => '',
    //         'AddressLine3' => ''
    //     ),
    //     'TYPE' => '1',
    //   'IS_MULTIPLE_TYPE' => '1',
    //     'ORIGINAL_FIELD_NAME' => ''
    //   );
    // $xpathArr['MailingAddress'] = array(
    //     'XPATH' => array(
    //         'Name' => '',
    //         'Address' => '',
    //         'Date' => ''
    //     ),
    //     'TYPE' => '1',
    //     'IS_MULTIPLE_TYPE' => '1',
    //     'ORIGINAL_FIELD_NAME' => ''
    //   );
      // $xpathArr['MailingAddress'] = array(
      //   'XPATH' => array(
      //       'AddressLine1' => '//label[text()="Registered Office"]/parent::div/following-sibling::div/label[text()="Address"]/parent::div/following-sibling::div[1]/span[1]/text()[normalize-space()]',
      //       'AddressLine2' => '//label[text()="Registered Office"]/parent::div/following-sibling::div/label[text()="Address"]/parent::div/following-sibling::div[1]/span[2]/text()[normalize-space()]',
      //       'AddressLine3' => '//label[text()="Registered Office"]/parent::div/following-sibling::div/label[text()="Address"]/parent::div/following-sibling::div[1]/span[3]/text()[normalize-space()]',
      //       'City' => '//label[text()="Registered Office"]/parent::div/following-sibling::div/div/label[text()="City, State Zip"]/parent::div/parent::div/following-sibling::div/div/span[1]/text()[normalize-space()]',
      //       'State' => '//label[text()="Principal Office "]/parent::div/following-sibling::div/label[text()="City, State Zip"]/parent::div/following-sibling::div[1]/span[2]/text()[normalize-space()]',
      //       'Zip' => '//label[text()="Principal Office "]/parent::div/following-sibling::div/label[text()="City, State Zip"]/parent::div/following-sibling::div[1]/span[3]/text()[normalize-space()]'
      //   ),
      //   'TYPE' => '1',
      // 'IS_MULTIPLE_TYPE' => '1',
      //   'ORIGINAL_FIELD_NAME' => 'Principal Office'
      // );

    // $xpathArr['Capitals'] = array(
    //   'XPATH' => array(
    //       'Type' => '',
    //       'Class' => '',
    //       'Value' => '',
    //       'NoOfShares' => ''
    //   ),
    //   'TYPE' => '1',
    //   'IS_MULTIPLE_TYPE' => '1',
    //   'ORIGINAL_FIELD_NAME' => ''
    // );

    // $xpathArr['Activities'] = array( 
    //   'XPATH' => '',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => '' 
    //  );
    //  $xpathArr['lastReportingYear'] = array( 
    //   'XPATH' => '//label[text()="Last Reporting Year"]/parent::div/following-sibling::div/span/text()[normalize-space()]',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'last Reporting Year' 
    //  );
    //  $xpathArr['NextReportDueDate'] = array( 
    //   'XPATH' => '//label[text()="Next Report Due Date"]/parent::div/following-sibling::div/span/text()[normalize-space()]',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Next Report Due Date' 
    //  );
     
    //additinal xpath properties (without match as above structure)
    
    // $xpathArr['ProtectedSeries'] = array(
    //   'XPATH' => array(
    //       'Business No.' => '(//table[@class="results display"])[12]/tr[*]/td[1]/text()',
    //       'Hierarchy' => '(//table[@class="results display"])[12]/tr[*]/td[2]/text()',
    //       'Name' => '(//table[@class="results display"])[12]/tr[*]/td[3]/text()',
    //       'Status' => '(//table[@class="results display"])[12]/tr[*]/td[4]/text()',
    //   ),
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '1',
    //   'ORIGINAL_FIELD_NAME' => 'Protected Series'
    // );
    // $xpathArr['FilingDate'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[6]/td[3]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Filing Date' 
    //  );
    // $xpathArr['Chapter'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[8]/td[1]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Chapter' 
    //  );
    // $xpathArr['Modified'] = array( 
    //   'XPATH' => '(//table[@ class = "results display"])[1]/tr[4]/td[3]/text()',
    //   'TYPE' => '0',
    //   'IS_MULTIPLE_TYPE' => '0',
    //   'ORIGINAL_FIELD_NAME' => 'Modified' 
    //  );

  return $xpathArr;
}
}
?>
