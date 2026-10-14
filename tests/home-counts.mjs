import test from 'node:test';
import assert from 'node:assert/strict';
import {homeCatalogCounts} from '../src/home-catalog-counts.js';

test('homepage includes reviewed additions and counts shared files once',()=>{
 const counts=homeCatalogCounts({
  forms:[{id:'form',file:'https://example.org/form.pdf'}],
  resources:[{id:'guide',file:'https://example.org/guide.pdf'}],
  reviewedBatch:[{id:'new',type:'Form',file:'https://example.org/new.pdf'},{id:'alias',file:'https://example.org/guide.pdf'}],
  members:[{id:'member'}]
 });
 assert.equal(counts.library,4);
 assert.equal(counts.forms,2);
});

test('reviewed file takes precedence over supplementary duplicate',()=>{
 const row={id:'collected-0123456789abcdef01234567',title:'Kaynak',type:'Rehber',level:'Lise',topic:'Rehberlik',file:'https://orgm.meb.gov.tr/guide.pdf',sourcePage:'https://orgm.meb.gov.tr/',sourceType:'official'};
 const counts=homeCatalogCounts({forms:[],resources:[],reviewedBatch:[{...row,id:'reviewed'}],supplementary:[row]});
 assert.equal(counts.library,1);
});
