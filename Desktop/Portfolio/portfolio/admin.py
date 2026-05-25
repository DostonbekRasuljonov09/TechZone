from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import SkillCategory, Tag, Project, ProjectImage, Message


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'featured', 'order', 'get_image')
    list_editable = ('featured', 'order')
    list_filter = ('category', 'featured')
    list_display_links = ('name',)
    search_fields = ('name', 'description', 'category__name')
    filter_horizontal = ('tags',)
    inlines = [ProjectImageInline]
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return mark_safe(f'<img src="{first_image.image.url}" style="width:150px; border-radius:8px;">')
        return "-"
    get_image.short_description = "Rasm"


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'text', 'created_at')


admin.site.register(Tag)

admin.site.site_header = "Portfolio Admin"
admin.site.site_url = "/"
admin.site.index_title = "Portfolio boshqaruvi"
admin.site.login_template = "admin/login.html"
