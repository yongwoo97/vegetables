from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    #admin 페이지에 커스텀
    #list_display는 admin에 보여주는 model의 칼럼
    #list_display = ['pk', 'user', 'nickname', 'nickname_length', 'position']

    #list_display는 상세 링크를 걸어줄 칼럼 이름
    #list_display_links = ['nickname']

    #어떤 칼럼을 기준으로 검색할지
    #search_fields = ['nickname']

    #어드민 우측에 필터 항목을 생성하여 명시한 칼럼의 종류들로 빠르게 필터링하는 도구를 제공한다
    #list_filter = ['position']


    #def nickname_length(self, account):
    #    return f"{len(account.nickname)} 글자"

    list_display = (
        'username', 'is_admin', 'is_active'
    )

    list_display_links = (
        'username',
    )