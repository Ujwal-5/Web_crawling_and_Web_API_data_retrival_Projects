<?php
set_time_limit(0);

if (!defined('nl')) 
{
   define('nl', chr(13).chr(10));
}
define('BROWSER_DIR', dirname(__FILE__));

/**
 * Emulates a webbrowser request to a webserver.
 * 
 * Usage:
 * 
 * $Browser = new Browser;
 * $Browser->fetchURL('http://www.astina.ch/');
 * print $Browser->getContent();
 * 
 * @author		Philipp Kraeutli <pkraeutli@astina.ch>
 * @copyright 	2005-2006 Astina AG
 */
class Browser
{   
	/**
	 * Sets caching on/off
	 * 
	 * @var bool
	 */
	public $caching = false;

	/**
	 * Sets logging on/off
	 * 
	 * @var bool
	 */ 
	public $log = false;

	/**
	 * URL used for the request. Consists of [scheme]:[port]//[host][path]
	 * 
	 * @var string
	 */
	public $url;

	/**
	 * If true, each request will be printed to the output
	 * 
	 * @var bool
	 */
	public $dump_request = false;
	
	/**
	 * Socket connection
	 * 
	 * @var resource
	 */
	private $connection = null;
	
	/**
	 * Protocol to be used for requests
	 * 
	 * @var string
	 */
	private $protocol = 'HTTP/1.1';
	
	/**
	 * Request to be sent
	 * 
	 * @var string
	 */
	private $request;

	/**
	 * Array containig reponse data recieved after the request has been sent
	 * 
	 * @var array(headers, content, forms)
	 */
	private $response;

	/**
	 * Request headers
	 * 
	 * @var string[]
	 */
	private $headers = array();

	/**
	 * Cookies array
	 * Example: $this->cookies['foo'] = 'bar'
	 * 
	 * @var string[]
	 */
	private $cookies = array();
	
	/**
	 * POST contents
	 * 
	 * @var string[]
	 */
	private $contents = array();

	/**
	 * Recieved response content. Same as $this->response['content']
	 * 
	 * @var string
	 */
	private $content;

	/**
	 * DOMDocument created, if possible, from response content
	 * 
	 * @var DOMDocument
	 */
	private $dom;

	/**
	 * DOMXPath created from $this->dom
	 * 
	 * @var DOMXPath
	 */
	private $xpath;

	/**
	 * Last fetched URL
	 * 
	 * @var string
	 */
	private $referer;

	/**
	 * Method used for request. Mostly GET or POST
	 * 
	 * @var string
	 */
	private $method;

	/**
	 * Scheme used for request. Mostly http
	 * 
	 * @var string
	 */
	private $scheme;

	/**
	 * Host to connect to for the connection and request
	 * 
	 * @var string
	 */
	private $host;

	/**
	 * Port to be used for the connection. Default ist 80
	 * 
	 * @var int
	 */
	private $port;

	/**
	 * Request path
	 * 
	 * @var string
	 */
	private $path;

	/**
	 * Transport protocol. Default is tcp
	 * 
	 * @var string
	 */
	private $transport;

	/**
	 * Integer to count redirections by Location response headers to avoid endless loops
	 * 
	 * @var int
	 */
	private $redirectCount = 0;
	
	/**
	 * Maximum number of redirections
	 * 
	 * @var int
	 */
	private $redirectCountMax = 5;
	
	public function __construct()
	{
		$this->headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)';
		$this->headers['Accept'] = 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5';
		$this->headers['Accept-Language'] = 'de-ch,de,en-us;q=0.5';
		$this->headers['Accept-Encoding'] = ''; //'gzip,deflate';
		$this->headers['Accept-Charset'] = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7';
		//$this->headers['Keep-Alive'] = '300';
		//$this->headers['Connection'] = 'keep-alive';
		$this->headers['Connection'] = 'close';
	}
   
	public function __destruct()
	{
		//var_dump($this->cookies);
		
	}
	
	/**
	 * Adds a request header to the header list (or replaces one)
	 * 
	 * @param string $header	header name
	 * @param string $value		header value
	 */
	public function setHeader($header, $value)
	{
		$this->headers[$header] = $value;
	}
	
	/**
	 * Returns the requested header or null, if the header is not set
	 * 
	 * @param string $header	header name
	 */
	public function getHeader($header)
	{
		return isset($this->headers[$header]) ? $this->headers[$header] : null;
	}

	/**
	 * Sets the content to be sent making a POST request
	 * 
	 * @param string $var	name of the variable or an array containing multiple content variables: array('var' => 'value')
	 * @param string $value	value of the variable
	 */
	public function setPostContent($var, $value = null)
	{
	    	if (is_array($var)) 
		{
				$this->contents = $var;
		} 
		elseif ($value === null) 
		{
			$contents = explode('&', $var);
			foreach ($contents as $cnt) 
			{
				list($var, $value) = explode('=', $cnt);
				$this->setPostContent($var, urldecode($value));
			}
		} 
		else 
		{
			$this->contents[$var] = $value;
		}
	}
	
	/**
	 * Sets a cookie
	 * 
	 * @param string $cookie	cookie name
	 * @param string $value		cookie value
	 * @param string $path		cookie path
	 * @param string $domain	cookie domain
	 */
	public function setCookie($cookie, $value, $path = '/', $domain = null)
	{		
		if (!$domain) 
		{
			$domain = $this->host;
		}
		$this->cookies[$domain][$path][$cookie] = $value;
	}
   
	/**
	 * Clears a cookie
	 * 
	 * @param string $cookie	cookie name
	 * @param string $path		cookie path
	 * @param string $domain	cookie domain
	 */
	public function clearCookie($cookie, $path = '/', $domain = null)
	{
		if (!$domain) 
		{
			$domain = $this->host;
		}
		if (isset($this->cookies[$domain][$path][$cookie]))
		{
			unset($this->cookies[$domain][$path][$cookie]);
		}
	}
  
	/**
	 * Returns a cookie
	 * 
	 * @param string $cookie	cookie name
	 * @param string $path		cookie path
	 * @param string $domain	cookie domain
	 * 
	 * @return string	cookie value
	 */
	public function getCookie($cookie, $path = '/', $domain = null)
	{
		if (!$domain) 
		{
			$domain = $this->host;
		}
		if (isset($this->cookies[$domain][$path][$cookie])) 
		{
			return $this->cookies[$domain][$path][$cookie];
		}
	}
   
	/**
	 * Returns the urlencoded cookie string for a given path and domain. Used directly for a request.
	 * 
	 * @param string $path		cookie path
	 * @param string $domain	cookie domain
	 * 
	 * @return string
	 */
	public function getCookies($path = '/', $domain = null)
	{
		$cookies = array();
		if (!$domain) 
		{
			$domain = $this->host;
		}
		if (isset($this->cookies[$domain][$path])) 
		{
			foreach ($this->cookies[$domain][$path] as $var => $value) 
			{
				$cookies[] = $var.'='.urlencode($value);
			}
		}
		return implode('; ', $cookies);
	}
	
	/**
	 * Returns an array containing the cookies fot a given path and domain.
	 * 
	 * @param string $path		cookie path
	 * @param string $domain	cookie domain
	 * 
	 * @return string[]
	 */
	public function getCookiesArray($path = '/', $domain = null)
	{
		if (!$domain) 
		{
			$domain = $this->host;
		}
		
		if (isset($this->cookies[$domain][$path])) 
		{
			return $this->cookies[$domain][$path];
		}
		return array();
	}

	/**
	 * Tries to fetch the given URL and returns the fetched content.
	 * 
	 * @param string $url			URL to fetch
	 * @param string $method		method to be used
	 * @param string[] $contents	array containing post contents
	 * 
	 * @return string
	 */
	public function fetchURL($url, $method = 'GET', $contents = null)
	{
		echo $this->method = $method;
		echo "<BR>URL==".$url;
		
		if ($this->method == 'POST' && !$this->getHeader('Content-Type')) 
		{
			$this->setHeader('Content-Type', 'application/x-www-form-urlencoded');
		}
		if ($contents) 
		{
			$this->setPostContent($contents);
		}
		
		$this->parseURL($url);
		$this->createRequest();
		
		if (!$this->caching || !$this->readCache()) 
		{      
			$this->sendRequest();
			$this->readResponse();
		}
		
		$this->logRequest();
		$this->referer = $this->url;
		
		if ($this->headers['Connection'] == 'close')
		{
			$this->close();
		}
		
		$this->writeCache();
		
		// redirect?
		//echo "<pre>datattatta";
		//print_r($this->response['headers']);
		//echo  $this->getContent();
		if (isset($this->response['headers']['location'])) 
		{
			if ($this->redirectCount > $this->redirectCountMax) 
			{
				trigger_error('redirect count exceeded', E_USER_WARNING);
				$error = 'redirect count exceeded';
	    			throw new Exception($error);

				return false;
			}
			$url = $this->response['headers']['location'];
			if (!preg_match('/[a-z]+:\/\//', $url)) 
			{
				if ($url[0] != '/') $url = '/'.$url;
				$url = $this->scheme.'://'.$this->host.$url;
			}
			$this->redirectCount++;
			//echo "<br>PREEEEEEntttt".$url;
			#$this->fetchURL($url);
			//$cookieval=$this->response['headers']['set-cookie'].";".$this->response['headers']['arm_correlator'];
			$this->fetchURL($url);
		}
				exit();
		$this->redirectCount = 0;
      	
      		// dom & xpath
      		$this->getDOM();
      		$this->getXPath(true);
		
		/* @TODO: Return false if there was no 2xx status response resp in getContent() */      	
	
		return $this->getContent();
	}

	public function getResponce()
	{
		return $this->response['headers'];
	}

	public function fetchURL1($url, $method = 'GET', $contents = null, $cookieval)
	{
		echo "Cokkies Val".$cookieval;
		$this->method = $method;
				echo "<BR>URL==".$url;
		if($cookieval)
		{
			$this->headers['Cookie'] = $cookieval;
		}
		
		if ($this->method == 'POST' && !$this->getHeader('Content-Type')) 
		{
			$this->setHeader('Content-Type', 'application/x-www-form-urlencoded');
		}
		if ($contents) {
			$this->setPostContent($contents);
		}
		
		$this->parseURL($url);
		$this->createRequest();
		
		if (!$this->caching || !$this->readCache()) {      
			$this->sendRequest();
			$this->readResponse();
		}
		

		$this->logRequest();
		$this->referer = $this->url;
		
		if ($this->headers['Connection'] == 'close') {
			$this->close();
		}
		
		$this->writeCache();
		
		// redirect?
		//print_r($this->response['headers']);
		echo @"2====".$cookieval=$this->response['headers']['set-cookie'].";".$this->response['headers']['p3p'];
		//$this->fetchURL2($url, $method = 'GET', $contents = null, $cookieval);
		if (isset($this->response['headers']['location'])) {
			if ($this->redirectCount > $this->redirectCountMax) {
				//trigger_error('redirect count exceeded', E_USER_WARNING);
				return false;
			}
			$url = $this->response['headers']['location'];
			if (!preg_match('/[a-z]+:\/\//', $url)) {
				if ($url[0] != '/') $url = '/'.$url;
				$url = $this->scheme.'://'.$this->host.$url;
			}
			$this->redirectCount++;
			$this->fetchURL1($url,'GET',null,$cookieval);
			
		}
		$this->redirectCount = 0;
      	
      		// dom & xpath
      		$this->getDOM();
      		$this->getXPath(true);
		
		/* @TODO: Return false if there was no 2xx status response resp in getContent() */      	
	
		return $this->getContent();
	}
	
	public function fetchURL2($url, $method = 'GET', $contents = null, $cookieval)
	{
		echo $url;
		echo "2______>222".$this->method = $method;
		if($cookieval)
		{
			$this->headers['Cookie'] = $cookieval;
		}
		
		if ($this->method == 'POST' && !$this->getHeader('Content-Type')) 
		{
			$this->setHeader('Content-Type', 'application/x-www-form-urlencoded');
		}
		if ($contents) {
			$this->setPostContent($contents);
		}
		
		$this->parseURL($url);
		$this->createRequest();
		
		if (!$this->caching || !$this->readCache()) {      
			$this->sendRequest();
			$this->readResponse();
		}
		

		$this->logRequest();
		$this->referer = $this->url;
		
		if ($this->headers['Connection'] == 'close') {
			$this->close();
		}
		
		$this->writeCache();
		
		// redirect?
		print_r($this->response['headers']); 
		if (isset($this->response['headers']['location'])) {
			if ($this->redirectCount > $this->redirectCountMax) {
				//trigger_error('redirect count exceeded', E_USER_WARNING);
				return false;
			}
			$url = $this->response['headers']['location'];
			if (!preg_match('/[a-z]+:\/\//', $url)) {
				if ($url[0] != '/') $url = '/'.$url;
				$url = $this->scheme.'://'.$this->host.$url;
			}
			$this->redirectCount++;
			$this->fetchURL2($url,'GET',null,$cookieval);
			
		}
		$this->redirectCount = 0;
      	
      		// dom & xpath
      		$this->getDOM();
      		$this->getXPath(true);
		
		/* @TODO: Return false if there was no 2xx status response resp in getContent() */      	
	
		return  $this->getContent();
	}
   
   
	/**
	 * Returns the previously fetched content, if available
	 * 
	 * @return string
	 */
	public function getContent()
	{
		return isset($this->response['content']) ? $this->response['content'] : null;
	}
	
	/**
	 * Prints $this->getContent()
	 */
	public function dumpContent()
	{
		print $this->getContent();
	}

	/**
	 * Returns the response content's charset or ISO-88591-1, if non available.
	 * Searches first for a Content-Type header and second for a Content-Type Meta Tag
	 * 
	 * @return string
	 */
	public function getCharset()
	{
		if (isset($this->response['headers']['content-type'])
		   && preg_match('/; ?(.+)/', $this->response['headers']['content-type'], $matches)) 
		{
		   return $matches[1];
		}
		if (preg_match('/charset=(.+?)"/', $this->response['content'], $matches)) 
		{
		   return $matches[1];
		}
		return 'ISO-8859-1';
	}
   
	/**
	 * Sets the value for a HTML form input, if the form ist available in the response content.
	 * 
	 * @param string $form	form name or index (same as used in javascript document.forms[...]
	 */
	public function setFormVar($form, $var, $value)
	{
		if (!isset($this->response['forms']))
		{
			$this->getForms();
		}
		if (isset($this->response['forms'][$form])) 
		{      
			$this->response['forms'][$form]['vars'][$var] = $value;
		} 
		else 
		{
			//trigger_error('form '.$form.' not found in '.$this->url, E_USER_WARNING);
			$error = 'setFormVar: form '.$form.' not found in '.$this->url;
	    		throw new Exception($error);	
		}
	}
	
	public function setFormAction($form, $action)
	{
		if (!isset($this->response['forms'])) 
		{
			$this->getForms();
		}
		if (isset($this->response['forms'][$form])) 
		{      
			$this->response['forms'][$form]['action'] = $action;
		} 
		else 
		{
			//trigger_error('form '.$form.' not found in '.$this->url, E_USER_WARNING);
			$error = 'setFormAction: form '.$form.' not found in '.$this->url;
	    		throw new Exception($error);
		}
	}

	/**
	 * Submits the given form.
	 *
	 * @param string $form	form name or index (same as used in javascript document.forms[...]
	 * 
	 * @return string
	 */
	public function submitForm($form,$method,$cokkie)
	{
		if (!isset($this->response['forms'])) 
		{
			$this->getForms();
    		}
		if (isset($this->response['forms'][$form])) 
		{
			$this->setHeader('Content-Type', $this->response['forms'][$form]['enctype']);
			return $this->fetchURL1($this->response['forms'][$form]['action'], 
								   $this->response['forms'][$form]['method'], 
								   $this->response['forms'][$form]['vars'],$cokkie);
		} 
		else 
		{
			//trigger_error('form '.$form.' not found in '.$this->url, E_USER_WARNING);
			$error = 'submitForm: form '.$form.' not found in '.$this->url;
	    		throw new Exception($error);
		}
	}
    
	/**
	 * Searches the response for HTML forms and creates an array containing forms, inputs and default input values.
	 *
	 * @return string[]
	 */
	public function getForms()
	{     
		$this->response['forms'] = array();
		   
		$this->getDOM();
		   
		$this->xpath = new DOMXPath($this->dom);
		$nl = $this->xpath->query('//form');
		$i = 0;
		foreach ($nl as $form) 
		{
			$name = $form->getAttribute('name');
			$method = $form->getAttribute('method');
			if (stripos($method, 'post') === 0) 
			{
				$method = 'POST';
			} else 
			{
				$method = 'GET';
			}
			$action = $form->getAttribute('action');
			if (!preg_match('/[a-z]+:\/\//', $action))
			{
				if (strlen($action) > 0 and $action[0] != '/')
				{
					$action = dirname($this->path).'/'.$action;
					$action = str_replace('//', '/', $action);
				} elseif ($action == '') 
				{
					$action = $this->path;
				}
				$action = $this->scheme.'://'.$this->host.$action;
				//echo $i.': ' .$action;
			}
			$enctype = $form->getAttribute('enctype');
			if (!$enctype) 
			{
				$enctype = 'application/x-www-form-urlencoded';
			}
			$this->response['forms'][$i] = array('name' => $name, 'method' => $method ? $method : 'GET', 'action' => $action ? $action : $this->url, 'enctype' => $enctype);
			if (!empty($name)) 
			{
				$this->response['forms'][$name] =& $this->response['forms'][$i];
			}
			$vars = array();
			$inputs = $this->xpath->query('//input', $form);
			foreach ($inputs as $input) 
			{
				if (($input->getAttribute('type') == 'radio' && $input->getAttribute('checked'))
					|| ($input->getAttribute('type') == 'checkbox' && $input->getAttribute('checked'))
					|| $input->getAttribute('type') == 'text' || $input->getAttribute('type') == 'hidden') 
				{
					$vars[$input->getAttribute('name')] = $input->getAttribute('value');				
				}
			}
			$inputs = $this->xpath->query('//textarea', $form);
			foreach ($inputs as $input) 
			{
				$vars[$input->getAttribute('name')] = $input->nodeValue;
			}
			$inputs = $this->xpath->query('//select', $form);
			foreach ($inputs as $input) 
			{
				foreach ($this->xpath->query('option', $input) as $option) 
				{
					if ($option->getAttribute('selected')) 
					{
						$vars[$input->getAttribute('name')] = $option->getAttribute('value') ? $option->getAttribute('value') : $option->nodeValue;
					}
				}
			}
			$this->response['forms'][$i]['vars'] = $vars;
			$i++;
		}

		return $this->response['forms'];
	}

	/**
	 * Returns the DOMDocument of the response content
	 * 
	 * @return DOMDocument
	 */
	public function getDOM()
	{
		//$this->dom = new DOMDocument('1.0', $this->getCharset());
		$this->dom = new DOMDocument('1.0', 'UTF-8');
		@$this->dom->loadHTML($this->getContent());
		return $this->dom;
	}
	
	/**
	 * Returns the DOMXPath of $this->dom
	 * 
	 * @return DOMXPath
	 */
	public function getXPath($recreate = false)
	{
		if ($recreate || !isset($this->xpath)) 
		{
			$this->xpath = new DOMXPath($this->getDOM());
		}
		return $this->xpath;
	}
   
	private function createRequest()
	{
		// prepare content
		if ($this->method == 'POST' && sizeof($this->contents) > 0) 
		{
			$content = $this->parseContent();
		}
		// request
		if (empty($this->path)) 
		{
			//trigger_error('path empty', E_USER_WARNING);
			$error = 'path empty';
			throw new Exception($error);
		}
		$req  = $this->method.' '.$this->path.' '.$this->protocol.nl;
		$req .= 'Host: '.$this->host.($this->port == 80 ? '' : ':'.$this->port).nl;

		// headers
		foreach ($this->headers as $header => $value)
		{
			$req .= $header.': '.$value.nl;
		}

		// referer
		if (!empty($this->referer)) 
		{
			$req .= 'Referer: '.$this->referer.nl;
		}

		// cookies
		if (sizeof($this->getCookiesArray()) > 0) 
		{
			$cookies = array();
			foreach ($this->getCookiesArray() as $cookie => $value) { $cookies[] = $cookie.'='.$value; }
				$req .= 'Cookie: '.implode('; ', $cookies).nl;
		}

		// content
		if (isset($content)) 
		{
			$req .= 'Content-Length: '.strlen($content).nl;
			$req .= nl.$content.nl;
		}

		// clear content
		$this->contents = array();

		$this->request = $req;
	}
   
	private function sendRequest()
	{
		// check connection
		if (!$this->connection) 
		{
			$this->connect();
		}

		if ($this->dump_request)
		{
			print("<pre>sending request:\n\n".$this->request.'</pre>');
			flush();
		}

		fwrite($this->connection, $this->request.nl);
	}

	private function readResponse()
	{
		$this->response = array();

		if (empty($this->connection)) 
		{
		 	return false;
		}

		$this->readResponseHeaders();

		$this->response['content'] = '';

		if (isset($this->response['headers']['transfer-encoding'])
		 && $this->response['headers']['transfer-encoding'] == 'chunked') 
		{
		 	$this->readResponseChunked();
		} 
		elseif (isset($this->response['headers']['content-length'])) 
		{
		 	$this->readResponseLength($this->response['headers']['content-length']);
		} 
		else 
		{
			$this->readResponseTillEOF();
		}

		$this->processContent();
	}

	private function readResponseHeaders()
	{
		if (empty($this->connection)) 
		{
			return false;
		}

		$this->response['headers']['raw'] = '';

		$streamData = stream_get_meta_data($this->connection);
		while (!$streamData['eof']) 
		{
			$streamData = stream_get_meta_data($this->connection);
			if ($streamData['timed_out']) 
			{
				exit('timeout');
			}
			$line = fgets($this->connection);
			$this->response['headers']['raw'] .= $line;
			$line = trim($line);
		 	if (empty($line))
			{
				return;
			}
		 	if (preg_match('/(.*?):\040?(.*)/', $line, $matches)) 
			{
		    		$this->response['headers'][strtolower($matches[1])] = trim($matches[2]);
		    		if (strtolower($matches[1]) == 'set-cookie' && preg_match('/(.+?)=(.+?);/', $matches[2], $m)) 
				{
		       			$this->setCookie($m[1], urldecode($m[2]), '/', $this->host);
		    		}
		 	}
		}
	}

	private function readResponseChunked()
	{
		while (!feof($this->connection)) 
		{
			$streamData = stream_get_meta_data($this->connection);
			if ($streamData['timed_out'])
			{
				exit('timeout');
			}
			$chunkSize = trim(fgets($this->connection));
			if ($chunkSize === '0') 
			{
				fgets($this->connection);
				break;
			}
			$chunkSize = hexdec($chunkSize);
			$chunk = '';
			while (!feof($this->connection) && strlen($chunk) < $chunkSize) 
			{
				$chunk .= fgets($this->connection);
			}
			$this->response['content'] .= trim($chunk);
		}
	}

	private function readResponseLength($length)
	{
		$content = '';
		while (!feof($this->connection) && strlen($content) < $length) 
		{
			$content .= fgets($this->connection);
		}
		$this->response['content'] = $content;
		}

		private function readResponseTillEOF()
		{
		$content = '';
		while (!feof($this->connection)) 
		{
		 	$content .= fgets($this->connection);
		}
		$this->response['content'] = $content;
		}

		private function processContent()
		{
		if (!isset($this->response['content']))
		{
			return;
		}

		$encoding = isset($this->response['headers']['content-encoding']) ? $this->response['headers']['content-encoding'] : null;

		switch ($encoding) 
		{
			case 'gzip' :
			$this->content = gzuncompress($this->response['content']);
			break;

			default :
			$this->content = $this->response['content'];				
		}
	}

	private function connect()
	{
		$this->close();
		$con = fsockopen($this->transport.'://'.$this->host,$this->port, $errno, $errstr, 50);
		     //or trigger_error('connection to '.$this->host.':'.$this->port.' failed', E_USER_WARNING);
		if (!$con) 
		{
			$error = 'connection to '.$this->host.':'.$this->port.'failed';
			throw new Exception($error);

		}
		 
		//stream_socket_enable_crypto($con,1);
		if ($con) 
		{
		 	$this->connection = $con;
		}
	}

	public function close()
	{
		if ($this->connection) 
		{
		 	fclose($this->connection);
		}
		$this->connection = null;
	}

	public function GetFormElementValues($frmname)
	{
		$arr_element_id = array();
		   
		$this->getDOM();
		   
		$this->xpath = new DOMXPath($this->dom);
		$nl = $this->xpath->query('//form');
		$i = 0;
		foreach ($nl as $form) 
		{
			$name = $form->getAttribute('name');
			if($frmname == $name)
			{		
					$vars = array();
					$inputs = $this->xpath->query('//input', $form);
					foreach ($inputs as $input) 
					{
						if (($input->getAttribute('type') == 'radio' && $input->getAttribute('checked'))
							|| ($input->getAttribute('type') == 'checkbox' && $input->getAttribute('checked'))
							|| $input->getAttribute('type') == 'text' || $input->getAttribute('type') == 'hidden') 
						{
							if($input->getAttribute('id') !='')
								$vars[$input->getAttribute('id')] = $input->getAttribute('value');				
							else
								$vars[$input->getAttribute('name')] = $input->getAttribute('value');				
						}
					}
					$inputs = $this->xpath->query('//textarea', $form);
					foreach ($inputs as $input) 
					{
						$vars[$input->getAttribute('id')] = $input->nodeValue;
					}
					$inputs = $this->xpath->query('//select', $form);
					foreach ($inputs as $input) 
					{
						foreach ($this->xpath->query('option', $input) as $option) 
						{
							if ($option->getAttribute('selected')) 
							{
								if($input->getAttribute('id') !='')
								{
									$vars[$input->getAttribute('id')] = $option->getAttribute('value') ? $option->getAttribute('value') : $option->nodeValue;
								}
								else
								{
									$vars[$input->getAttribute('id')] = $option->getAttribute('value') ? $option->getAttribute('value') : $option->nodeValue;
								}
							}
						}
					}
					$arr_element_id = $vars;
					$i++;
			}
		}

		return $arr_element_id;


	}   
	private function parseURL($url)
	{
		$this->url = $url;
		$url = parse_url($url);

		$this->host = $url['host'];
		if (isset($url['port'])) 
		{
			$this->port = $url['port'];
		}
		$this->path = isset($url['path']) ? $url['path'] : null;
		if (empty($this->path)) 
		{
			$this->path = '/';
		}
		if (isset($url['query'])) 
		{
			$this->path .= '?'.$url['query'];
		}
		$this->scheme = isset($url['scheme']) ? $url['scheme'] : 'http';

		switch ($this->scheme) 
		{
			case 'https' :
			$this->transport = 'ssl';
			if (!isset($this->port)) $this->port = 443;
			break;
			default :
			$this->transport = 'tcp';
			if (!isset($this->port)) $this->port = 80;
		}
	}

	private function readCache()
	{
		$headers_cache_file = BROWSER_DIR.'/cache/'.crc32($this->request).'-'.strftime('%Y%m%d%H').'.headers.txt';
		$content_cache_file = BROWSER_DIR.'/cache/'.crc32($this->request).'-'.strftime('%Y%m%d%H').'.content.html';

		if (!file_exists($headers_cache_file)) 
		{
		 return false;
		}

		$this->response['headers']['raw'] = file_get_contents($headers_cache_file);
		$this->response['content'] = file_get_contents($content_cache_file);

		foreach (explode("\n", $this->response['headers']['raw']) as $line) 
		{
		 	if (preg_match('/(.*?):\040?(.*)/', trim($line), $matches)) 
			{
		    		$this->response['headers'][strtolower($matches[1])] = $matches[2];
		    		if ($matches[1] == 'Set-Cookie' && preg_match('/(.+?)=(.+?);/', $matches[2], $m)) 
				{
		       			$this->setCookie($m[1], $m[2]);
		    		}
		 	}
		}
	}

	private function writeCache()
	{
		if (!$this->caching) 
		{
		 return;
		}      

		$request_cache_file = BROWSER_DIR.'/cache/'.crc32($this->request).'-'.strftime('%Y%m%d%H').'.request.txt';
		$headers_cache_file = BROWSER_DIR.'/cache/'.crc32($this->request).'-'.strftime('%Y%m%d%H').'.headers.txt';
		$content_cache_file = BROWSER_DIR.'/cache/'.crc32($this->request).'-'.strftime('%Y%m%d%H').'.content.html';

		file_put_contents($request_cache_file, $this->request);
		file_put_contents($headers_cache_file, $this->response['headers']['raw']);
		file_put_contents($content_cache_file, $this->response['content']);
		}

		private function logRequest()
		{
		if (!$this->log)
		{
			return;
		}

		$fp = fopen(BROWSER_DIR.'/browser_'.strftime('%Y%m%d%H').'.log', 'a');
		flock($fp, LOCK_EX);
		$log  = '============================================================================'.nl;
		$log .= strftime('%Y-%m-%d %H:%M:%S').nl;
		$log .= $this->url.nl.nl;
		$log .= $this->request.nl;
		$log .= $this->response['headers']['raw'];
		fwrite($fp, $log);
		flock($fp, LOCK_UN);
		fclose($fp);
	}

	private function isMultipartPost()
	{
		$content_type = $this->getHeader('Content-Type');
		return strpos($content_type, 'multipart/form-data') === 0;
	}

	private function parseContent()
	{
		if ($this->isMultipartPost()) 
		{
			return $this->parseContentMultipart();
		}

		$contents = array();
		foreach ($this->contents as $content => $value) 
		{
			$contents[] = urlencode($content).'='.urlencode($value);
		}
		$content = implode('&', $contents);

		return $content;
	}

	private function parseContentMultipart()
	{
		$boundary = '--------------------' . md5(microtime(true));
		$this->setHeader('Content-Type', 'multipart/form-data; boundary='.$boundary);

		$content = '';
		foreach ($this->contents as $name => $value) 
		{
			$content .= sprintf('--%s%sContent-Disposition: form-data; name="%s"%s%s%s%s',
				$boundary, nl, $name, nl, nl, $value, nl);
		}
		$content .= '--'.$boundary.'--';
		return $content;
	}
}

?>
