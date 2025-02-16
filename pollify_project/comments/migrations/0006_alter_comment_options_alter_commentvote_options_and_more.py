# Generated by Django 4.2.16 on 2025-02-01 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0005_commentvote_comment_voters'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='commentvote',
            options={'verbose_name': 'Comment Vote', 'verbose_name_plural': 'Comment Votes'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(help_text='User who created the comment.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(help_text='Content of the comment.'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='downvotes',
            field=models.PositiveIntegerField(default=0, help_text='Number of downvotes.'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='poll',
            field=models.ForeignKey(help_text='The poll this comment belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='polls.poll'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvotes',
            field=models.PositiveIntegerField(default=0, help_text='Number of upvotes.'),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(help_text='Comment being voted on.', on_delete=django.db.models.deletion.CASCADE, to='comments.comment'),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='user',
            field=models.ForeignKey(help_text='User who voted.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='vote_type',
            field=models.CharField(choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')], help_text='Type of vote.', max_length=10),
        ),
        migrations.AddIndex(
            model_name='commentvote',
            index=models.Index(fields=['user', 'comment'], name='comments_co_user_id_1a41f9_idx'),
        ),
    ]
