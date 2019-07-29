from alipay import AliPay
alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsNlcDS8XlMdOFGHSpMf0G4RVfGhJy/nhX3bm//PgPcFRv9M3eCP7zBO+gwBTdcLy0XVc/8o6DC6Hc+xy4UtSm7+LJu0Y2rN9E/uz6gXKtrYNkIZY9EFfp39oSM3ofip49BM+3p9dHd7w1HtF9lq2L4Yt+fpixr3vreciy5swHiDO8vEC17XdvQqda5NUblxSKt/QDF1so870Tl695y9QFU+DsXfpY2HeSCJIdMgsFzhs8rhzIT2vzOALTgOuWPxIQzAG5iaiktZSiJAV3N8Www7beYlCrjIvh/zaj/F1Ai5nxjoW5VUjiU7nDU7aYBKvpnkjXLh10xZqwZhsHx3uwQIDAQAB
-----END PUBLIC KEY-----"""
app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAsNlcDS8XlMdOFGHSpMf0G4RVfGhJy/nhX3bm//PgPcFRv9M3eCP7zBO+gwBTdcLy0XVc/8o6DC6Hc+xy4UtSm7+LJu0Y2rN9E/uz6gXKtrYNkIZY9EFfp39oSM3ofip49BM+3p9dHd7w1HtF9lq2L4Yt+fpixr3vreciy5swHiDO8vEC17XdvQqda5NUblxSKt/QDF1so870Tl695y9QFU+DsXfpY2HeSCJIdMgsFzhs8rhzIT2vzOALTgOuWPxIQzAG5iaiktZSiJAV3N8Www7beYlCrjIvh/zaj/F1Ai5nxjoW5VUjiU7nDU7aYBKvpnkjXLh10xZqwZhsHx3uwQIDAQABAoIBAA4YFIz8bs2toJxhO29kfCDhSArVKOR3sq1wBXLqlbl2ObSm+am6fGvEOw+nq/8bnUxyJQpBrKSh5KupcXJhFWFSP53HkY6EdXhtO+ZvtbsgAS6+dkJpH11y+vWqa1f6vI7/JaiKXNpvlRPqCyZaDmD1OZ7NhKfAJWTfoddGM+yCoM4fOSJekSXLuZYOLEFWJ/hzTfvp15T0PkDh00KxGGMEEvV0yqUKUIjViv7O8K8Aks7W5rKmUikAp6CpcahoEoGA3TeyH+womvNvYmw8iu/9z19SoAtwObG4jVRvE3/Wtsy0fJqJNj5mOiemeaEgjrGcaKORolM2ZS7XWpZgVdECgYEA6NXrSVtQMH0HL0YbYpVTlGx0xc9jb1VyZJ2ryZWMzpDZBdjVZ/7XGkJE8dCPYb+6ouUV+Bs97n/u5h0J/UcxOTnvrJaKzIzQ74V/HadbG340i6nDhli0p2M2pjOM4n882Yvlm+YVUOz9nuyuY4b/kI3TX4vJgd/0DCbA+2RnT9UCgYEAwnGFZLYzBR1Ey9Klj77wRKZKLejghuX4amJrfCkIpa8uMnxajEg2xs810SjCQCALQL6v+2m91zGmd1K+EzPrjy3x2JexB13gkmgRUdM+hSsI5/5V9z7htbqyJ8PXalL/WKKRlfQh1kG3ct+nBLbBeRPjXPxlOpYek3q2CnNNxT0CgYAIKDZuA3zzte2iglpDQegDsykEJRfetqejTsLN9SdRtVFlGwue8RaoHNo9fokHa6gmPNBgONQanvDHrwzCitP2pUj4Su3h7K0FNzAU4eAXPnyox/HJqyHpG1i2yeeNp9eB55zLsWvdwe/AuZoCcqBReCaHmmYc3rO2GUV5iTL1YQKBgCnp7JY0DDVrBLxm8NdWklZJ/i19SIDrq6vLAV5nPfzxESVC1wXsPxqF6hTnE1BdV++h6y9nsMtlYXvRMzXSeFGJ1tsYf8mVu+XzVuBrh8uO5kGT+pXsUR0qXGLj/VhnAbHqgTVwxaZ4zgGOImOKvZPK7LTLl0qUt4yU5A7GohoFAoGACCyrRGFTAyzcAV6jYsK+neRxmJogUV/zjzoohnU8eDH1v9Efehos0ixA2igPw7aTXE/D+foFbqC6SPGDp+NFeyVm/u04nlVXNKznN6w5MOG3up6iTuszs6yicZVenytENqwPCidYr0mQW4htSfZgzQG7hXkoYu9xv8b2rAFaMO8=
-----END RSA PRIVATE KEY-----"""
# 实例化支付应用
alipay = AliPay(
    appid="2016093000627799",
    app_notify_url=None,  # 应用程序url通知
    app_private_key_string=app_private_key_string,  # 私钥
    alipay_public_key_string=alipay_public_key_string,  # 公钥
    sign_type="RSA2"  # 加密算法
)
# 发起支付请求
order_string = alipay.api_alipay_trade_page_pay(  # 网页支付请求
    out_trade_no="99999",  # 订单号
    total_amount=str(66666),  # 支付金额
    subject="生鲜交易",  # 交易主体
    return_url='http://127.0.0.1:8000/buyer/pay_result/',
    notify_url='http://127.0.0.1:8000/buyer/pay_result/'
    # notify通知公告,notify通知公告，notify
)
print("http://openapi.alipaydev.com/gateway.do?" + order_string)