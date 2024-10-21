from DrissionPage import ChromiumPage 
from RecaptchaSolver import RecaptchaSolver
import time

 
driver = ChromiumPage()
recaptchaSolver = RecaptchaSolver(driver)

driver.get("https://www.rp.gob.pa/LoginUsuario")
time.sleep(10)
t0 = time.time()
recaptchaSolver.solveCaptcha()
print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds")

driver.ele("#recaptcha-demo-submit").click()

driver.close()
