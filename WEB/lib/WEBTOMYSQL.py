import pymysql
import pymysql.cursors
from WEB.lib import SECRET


class CONNECT_TO_BDD:
    def __init__(self):
        ssl_settings = {'ca': '/etc/letsencrypt/live/bc.outuru.site/fullchain.pem',
                                            'cert': '/etc/letsencrypt/live/bc.outuru.site/fullchain.pem',
                                            'key': '/etc/letsencrypt/live/bc.outuru.site/privkey.pem'}
        self.connection = pymysql.connect(user="test",
                                     password="2^DBBaBwFFjbjfxYMg9FfB2CXee5L^8wpM2M6aWUwqnpSZnwJMss7zKH4Dp&",
                                     host="bdd.outuru.site",
                                     database="WEB",
                                     ssl_disabled=None,
                                     #ssl_verify_cert=True, ssl_verify_identity=True,
                                     #ssl=ssl_settings
                                          )
                                     # max_allowed_packet=(67108864)
        # self.connection.cursor()
        # self.connection.commit()
