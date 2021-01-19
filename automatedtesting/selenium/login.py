# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging, sys

# Start the browser and login with standard_user
def login (user, password):
    print ('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    #options = ChromeOptions()
    #options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome('D:\Chromedriver\chromedriver.exe')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, datefmt='%Y-%m-%d %H:%M:%S')
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    # Logging in to Website
    logging.info('Logging in to Website')
    driver.find_element_by_css_selector(
        'input[data-test="username"]').send_keys(user)
    driver.find_element_by_css_selector(
        'input[data-test="password"').send_keys(password)
    driver.find_element_by_css_selector('input[value=LOGIN]').click()
    
    # Checking Login
    logging.info('Searching for Products')
    product_id = driver.find_element_by_class_name('product_label').text
    assert "Products" in product_id, 'An Error occured during login'
    if 'Products' in product_id:
        print('User {} logged in successfully'.format(user))
    else:
        pass
    logging.info('User {} logged in successfully'.format(user))

    # Adding Items to cart 
    logging.info('Finding Products')
    products=driver.find_elements_by_css_selector('.inventory_item')
    obj_list=[]

    for p in products:
        # Searching for Product
        name=p.find_element_by_css_selector('.inventory_item_name').text
        obj_list.append(name)
        logging.info('{} Porduct found on Website'.format(name))

        # Adding to Cart 
        p.find_element_by_css_selector('button.btn_inventory').click()
        print('Product {} added to cart'.format(name))
        logging.info('Product {} added to cart'.format(name))
    print(len(obj_list))

    # Checking Cart 
    cart = driver.find_element_by_css_selector('.shopping_cart_badge').text
    print(cart)
    assert int(cart) == int(len(obj_list)), 'Not all Elements in Cart'
    if int(cart) == int(len(obj_list)):
        print('All Elements in Cart')
        logging.info('All Elements have been added to cart')
    else:
        print('Elements are Missing in Cart')
        logging.error('Check Elements in Cart')

    # Empty Cart 
    driver.find_element_by_css_selector('a.shopping_cart_link').click()
    cart_elements = driver.find_elements_by_css_selector('.cart_item')
    for c in cart_elements:
        cart_product = c.find_element_by_css_selector('.inventory_item_name').text
        c.find_element_by_css_selector('button.btn_secondary.cart_button').click()
        print('Product {} removed from cart'.format(cart_product))
        logging.info('Product {} removed from cart'.format(cart_product))
    
    # Check Cart
    driver.find_element_by_css_selector('a.btn_secondary').click()
    try:
        driver.find_element_by_css_selector('.shopping_cart_badge').text
        AssertionError: 'Cart not empty'
        logging.error('Cart is not empty')
    except: 
        print('Cart is empty')
        logging.info('Cart is empty again')

    print('Cart is empty again')
    logging.info('Test was successfull')

login('standard_user', 'secret_sauce')