# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Set'
        db.create_table(u'gatherer_set', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('magiccard_info_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'gatherer', ['Set'])

        # Adding model 'Card'
        db.create_table(u'gatherer_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title_pt', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_ct', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_cs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_jp', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_it', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_de', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_kr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_br', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('multiverseId_pt', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_es', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_ct', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_cs', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_fr', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_jp', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_ru', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_it', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_de', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_kr', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId_br', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('multiverseId', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('cost', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cmc', self.gf('django.db.models.fields.IntegerField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('flavor', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('strength', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gatherer.Set'])),
            ('collector_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('rarity', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'gatherer', ['Card'])

        # Adding M2M table for field printings on 'Card'
        db.create_table(u'gatherer_card_printings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_card', models.ForeignKey(orm[u'gatherer.card'], null=False)),
            ('to_card', models.ForeignKey(orm[u'gatherer.card'], null=False))
        ))
        db.create_unique(u'gatherer_card_printings', ['from_card_id', 'to_card_id'])

        # Adding model 'SubCard'
        db.create_table(u'gatherer_subcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title_pt', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_ct', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_cs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_jp', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_it', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title_de', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('flavor', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('strength', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('collector_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('card', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gatherer.Card'], unique=True, null=True)),
        ))
        db.send_create_signal(u'gatherer', ['SubCard'])


    def backwards(self, orm):
        # Deleting model 'Set'
        db.delete_table(u'gatherer_set')

        # Deleting model 'Card'
        db.delete_table(u'gatherer_card')

        # Removing M2M table for field printings on 'Card'
        db.delete_table('gatherer_card_printings')

        # Deleting model 'SubCard'
        db.delete_table(u'gatherer_subcard')


    models = {
        u'gatherer.card': {
            'Meta': {'object_name': 'Card'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cmc': ('django.db.models.fields.IntegerField', [], {}),
            'collector_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'flavor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'multiverseId': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'multiverseId_br': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_cs': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_ct': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_de': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_es': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_fr': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_it': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_jp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_kr': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_pt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'multiverseId_ru': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'printings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['gatherer.Card']", 'null': 'True', 'blank': 'True'}),
            'rarity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gatherer.Set']"}),
            'strength': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title_br': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_cs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_ct': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_it': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_jp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_kr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_pt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        u'gatherer.set': {
            'Meta': {'object_name': 'Set'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magiccard_info_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'gatherer.subcard': {
            'Meta': {'object_name': 'SubCard'},
            'card': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['gatherer.Card']", 'unique': 'True', 'null': 'True'}),
            'collector_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'flavor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title_cs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_ct': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_it': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_jp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_pt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['gatherer']