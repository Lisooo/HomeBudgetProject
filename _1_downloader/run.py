from app import db
from _1_downloader.main import main
from _1_downloader.drivers import FirefoxDriver
from _1_downloader.loggers import Logger
from process_log.utils import ProcessLog

if __name__ == "__main__":

    logger = Logger(__name__).logger()
    logger.info(f'Started'.upper())

    # import_log = ImportLogDatabase(db)
    # dates_range = import_log.generate_date_list_to_download()
    dates_range = ['2020-10-01', '2020-10-02']

    if dates_range:
        process_log = ProcessLog(db)
        process_log.start('HOMEBUDGET_DATA_DOWNLOADER', min(dates_range), max(dates_range))
        driver = FirefoxDriver().setup()  # setting driver instance

        try:
            main(driver, dates_range)    # MAIN process
            process_log.finish('RUNOK')
            logger.info(f'Ended successful'.upper())

        except Exception as e:
            db.session.rollback()
            process_log.finish('RUNFAILED')
            logger.error(f'Failed'.upper())
            logger.error(f'{e.args}')

        finally:
            db.session.close()
            driver.close()
            driver.quit()
    else:
        db.session.close()
        logger.info(f"There's no data to download")
        logger.info(f"Ended successful".upper())
