from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import time
from selenium.webdriver.common.by import By
import os
import requests
import io
from datetime import datetime as dt
from unidecode import unidecode

# Google search URLS

google_urls = [
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=wn3YaNVKcBy-QM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=AAOsXUGogQFt9M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=_sMJkto9zGngBM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=Y1oQUSeEMMBlTM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=IkeShz6phdsKsM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=5zkJ4QRDit9hRM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=XK0LjzuBhyTqhM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=p2H3g0VUmgaOsM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=iCTf0loOqBqk4M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=ff__74mUfnd08M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=E7xrWY5D2sAtZM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=dAEo3uyuU4ji-M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=nhO5Xe13zW4GVM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=Na9sUYpbBozUKM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=ZhmkddW0X25JtM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=43BwnVdKjglLrM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=wyskL1zKZxnd1M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=cRrVP51KdmNODM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=bsOhdZdM9LatTM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=8fjkw02TK_hyUM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=MX6Y6i86GrqdFM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=-6poiU4T3Z0BrM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=XPiWRCQW8jAdmM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=-iYXygwPbj6O3M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=LgEPL5fIBmCxhM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=Pgew_DTJaajSmM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=pKScZ2jOHAdNCM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=2qtYAC1SYUHPuM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=Dk-6YJMAyX7vUM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=RQzIR-OnZQMK7M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=udqNCQzZ2YfgjM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=_JpxN3xJ9o4GaM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=8M4k70BpXVvIEM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=nV2DxngRGuh9YM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=QNQ7dUiy0gbgFM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=-h3orTv-GxEzXM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=HHgskO3OAGvcTM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=lpvaEGw62Nz5bM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=0BHoo3fNWoMU_M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=inl3nf2ITJBN_M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=CCd3elVGj0CkWM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=tOvrGn9JBrsnAM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=QTZzPi5IDYMQwM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=A-uRXJVi973xaM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=UMQXccoC_q9yGM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=8nJzAnWULabYQM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=OK1knfpxLQiKSM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=AmvyZvvosFy6uM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=4hC63AIBrGj3pM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=5SmPBJTenR9i7M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=CyNgImwFrxmpHM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=n7JGQV3wqiEvIM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=HU--R6Nrw8zCrM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=bWpefknUNWROpM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=d0mDe10jZF3MTM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=89WtZtFS27dVVM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=le8GgCb5u48PGM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=C6hAqWO9qxyCoM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=nl6za_2_BFfV3M',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=AgLJjqUxIbZOCM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=9oh6S5DvrW6wQM',
    'https://www.google.com/search?q=namaste+gesture&sxsrf=ALiCzsYjq_Dd8DV2fMDbiXGrnxSG6YeIJQ:1658766990571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjGq_PJvJT5AhV6m_0HHUB4BVYQ_AUoAXoECAIQAw&biw=1920&bih=961&dpr=1#imgrc=pddvw8YOTW5AdM',
]
labels = ['namaste']

def get_images_from_google(wd, delay, max_images, lbl):

    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    image_urls = set()
    skips = 0
    for url in google_urls:
        print(len(image_urls))
        try:
            wd.get(url)
        except:
            print("url skipped")
            continue
        wd.implicitly_wait(2)
        images = wd.find_elements(By.CLASS_NAME, "n3VNCb")  # this is for main images
        #if i == 0:         # in the case of the first image in google search (the preview image),
        #    image = images[0]                  # the correspondent element in images is the first one, otherwise it is the second
        #else:
        #    image = images[1]
        #print(len(images),images)
        for i,image in enumerate(images):
            try:
                imageURL = image.get_attribute('src')  # if the image url is different prom preview image url, then we correcly loaded it
            except:
                print("image skipped")
                continue

            if imageURL in image_urls:  # check if that image is already present in image_urls set, if yes skip
                max_images += 1
                skips += 1

            elif imageURL and 'http' in imageURL:  # check if we can download the image
                if lbl in unidecode(image.get_attribute('alt').casefold()):  # check if the image caption contains word label in a case and accent insensitive way
                    image_urls.add(imageURL)

        suggested_images = wd.find_elements(By.CLASS_NAME,"lxa62b")  # it opens another page with suggested images
        try:
            suggested_images[0].click()
            time.sleep(1)
        except:
            continue
        scroll_down(wd)  # take suggested images
        scroll_down(wd)
        scroll_down(wd)
        sug_thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
        #print(len(sug_thumbnails))
        for sug_img in sug_thumbnails:
            try:
                sug_img.click()
                time.sleep(delay)
            except:
                continue

            sug_images = wd.find_elements(By.CLASS_NAME, "n3VNCb")  # this is for main images

            if sug_thumbnails.index(sug_img) == 0:  # in the case of the first image in google search (the preview image),
                sug_image = sug_images[0]  # the correspondent element in images is the first one, otherwise it is the second
            else:
                sug_image = sug_images[1]
            try:
                sug_imageURL = sug_image.get_attribute('src')  # if the image url is different prom preview image url, then we correcly loaded it
            except:
                print("image skipped")
                continue

            if sug_imageURL in image_urls:  # check if that image is already present in image_urls set, if yes skip
                #max_images += 1
                skips += 1

            elif sug_imageURL and 'http' in sug_imageURL:  # check if we can download the image
                if lbl in unidecode(sug_image.get_attribute('alt').casefold()):  # check if the image caption contains word label in a case and accent insensitive way
                    image_urls.add(sug_imageURL)
    return image_urls


def download_image(down_path, url, file_name, image_type='JPEG',verbose=True):
    try:
        time = dt.now()
        curr_time = time.strftime('%H:%M:%S')
        #Content of the image will be a url
        img_content = requests.get(url).content
        #Get the bytes IO of the image
        img_file = io.BytesIO(img_content)
        #Stores the file in memory and convert to image file using Pillow
        image = Image.open(img_file)
        file_pth = down_path + file_name

        with open(file_pth, 'wb') as file:
            image.save(file, image_type)

        if verbose == True:
            print(f'The image: {file_pth} downloaded successfully at {curr_time}.')
    except Exception as e:
        print(f'Unable to download image from Google Photos due to\n: {str(e)}')

def func():
    wd = webdriver.Chrome()

    path = 'C:/Users/enzop/Desktop/DS/'
    google_images_url = 'https://www.google.com/'
    # Make the directory if it doesn't exist
    for lbl in labels:
        if not os.path.exists(path + lbl):
            print(f'Making directory: {str(lbl)}')
            os.makedirs(path+lbl)

    accept=True     #for accepting the conditions that are shown during first iteration

    for lbl in labels:
        wd.get(google_images_url)
        #time.sleep(100)
        if accept:
            accept_button =  wd.find_elements("xpath","""//*[@id="L2AGLb"]/div""")
            accept = False
            try:
                accept_button[0].click()
            except:
                raise ValueError("Can't push the button")
        # Once we have added our urls to empty set then
        urls = get_images_from_google(wd,0.2, 1200, lbl)
        for i, url in enumerate(urls):
            download_image(down_path=f'{path}{lbl}/',
                        url=url,
                        file_name=str(i+1)+ '.jpg',
                        verbose=True)
    wd.quit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    func()