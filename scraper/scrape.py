from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, InvalidSessionIdException, TimeoutException, ElementClickInterceptedException
import re
import time
import pandas as pd

def split_genres(genres_text):
    # Use regex to split genres based on capital letters
    genres_list = re.findall('[A-Z][^A-Z]*', genres_text)
    return ', '.join(genres_list)

def save_to_csv(data, csv_file_path):
    # Save data to CSV file
    data.to_csv(csv_file_path, mode='a', header=False, index=False)

def main():
    driver = webdriver.Chrome()

    url = "https://www.imdb.com/search/title/?title_type=feature"
    driver.get(url)

    # Wait for the grid view button to be present
    grid_view_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "list-view-option-grid"))
    )

    grid_view_button.click()

    time.sleep(10)

    xpath_pattern_details_button = "//div[@class='ipc-poster-card__actions']//button[@class='ipc-btn ipc-btn--full-width ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--on-accent2 ipc-secondary-button gli-button']"
    
    # Number of times to click the "See more" button
    see_more_clicks = 280  # You can change this number

    # Click the "See more" button a specified number of times
    for _ in range(see_more_clicks):
        try:
            see_more_button = driver.find_element(By.CSS_SELECTOR,
                                                  "button.ipc-btn.ipc-btn--single-padding.ipc-btn--center-align-content.ipc-btn--default-height.ipc-btn--core-base.ipc-btn--theme-base.ipc-btn--on-accent2.ipc-text-button.ipc-see-more__button")

            # # Scroll to the "See more" button
            # driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)

            # Click the "See more" button using JavaScript
            driver.execute_script("arguments[0].click();", see_more_button)

            # Wait for the page to load after clicking "See more"
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "button.ipc-spinner.ipc-spinner--overlay.is-active"))
            )

            time.sleep(2)

        except:
            # If no "See more" button is found or clicked, break the loop
            break
    
    time.sleep(10)

    # Starting movie number
    start_movie = 12622

    # Number of movies to collect
    num_movies_to_collect = 1380

    # movie_data_list = []

    # Load existing data from the CSV file (if it exists)
    csv_file_path = 'movie_data.csv'
    try:
        existing_data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

        
    # Counter variable to keep track of the number of movies collected
    n = 0

    # Collect details for the specified range of movies
    for movie_number in range(start_movie, start_movie + num_movies_to_collect):
        
        
        # Find the details button for the current movie
        details_button_xpath = f"({xpath_pattern_details_button})[{movie_number}]"
        details_button = WebDriverWait(driver, 70).until(
            EC.presence_of_element_located((By.XPATH, details_button_xpath))
        )

        try:
            # Scroll into view to make sure the button is clickable
            # driver.execute_script("arguments[0].scrollIntoView(true);", details_button)

            # Use JavaScript to click the button
            driver.execute_script("arguments[0].click();", details_button)

            # Wait for the page to load after clicking "See more"
            # WebDriverWait(driver, 10).until(
            #     EC.invisibility_of_element_located((By.CSS_SELECTOR, "button.ipc-spinner.ipc-spinner--overlay.is-active"))
            # )

            # Switch to the pop-up window
            pop_up_window_handle = driver.window_handles[-1]
            driver.switch_to.window(pop_up_window_handle)

            # Wait for the description element to be present
            try:
                description_element = WebDriverWait(driver, 70).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sc-7316798c-2"))
                )
            except TimeoutException:
                # If there's a timeout waiting for the element, print a message and close the pop-up
                print(f"Timeout waiting for description element for movie {movie_number}. Closing pop-up.")
                close_button = WebDriverWait(driver, 70).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ipc-promptable-base__close"))
                )
                close_button.click()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                continue

            # Get the description text
            description = description_element.text.strip()

            # Find the title element
            try:

                title_element = WebDriverWait(driver, 70).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ipc-title.ipc-title--baseAlt.ipc-title--title.ipc-title--on-textPrimary.sc-a78ec4e3-3.cXtCdS h3.ipc-title__text.prompt-title-text"))
                )
            except TimeoutException:
                # If there's a timeout waiting for the element, print a message and close the pop-up
                print(f"Timeout waiting for genres element for movie {movie_number}. Closing pop-up.")
                close_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ipc-promptable-base__close"))
                )
                close_button.click()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                continue

            # Get the title text
            title = title_element.text.strip()

            # Wait for the genres element with data-testid=btp_gl
            try:
                genres_element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-testid='btp_gl']"))
                )
            except TimeoutException:
                # If there's a timeout waiting for the element, print a message and close the pop-up
                print(f"Timeout waiting for genres element for movie {movie_number}. Closing pop-up.")
                close_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ipc-promptable-base__close"))
                )
                close_button.click()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                continue

            # Get the genres text and split based on capital letters
            genres = split_genres(genres_element.text.strip())

            # Create a DataFrame with the current movie's data
            movie_data = pd.DataFrame({
                'Title': [title],
                'Description': [description],
                'Genres': [genres]
            })


            # Append data for the current movie to the CSV file
            save_to_csv(movie_data, csv_file_path)

            # Increment the counter
            n += 1
            # Print the number of data being collected
            print(f"{n} movies collected")

            # Find the close button and click to close the pop-up
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ipc-promptable-base__close"))
            )
            close_button.click()

            # Switch back to the main window
            driver.switch_to.window(driver.window_handles[0])

            # Wait for the page to load before finding the next button
            # time.sleep(1)

        except StaleElementReferenceException:
            # If the element is stale, find the details buttons again
            details_buttons = driver.find_elements(By.XPATH, xpath_pattern_details_button)

        except InvalidSessionIdException:
            # If the session id is invalid, the browser might have been closed, break the loop
            break

        except ElementClickInterceptedException:
            # If element click is intercepted, print a message and move on to the next iteration
            print(f"Element click intercepted for movie {movie_number}. Skipping to the next one.")
            continue

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()
