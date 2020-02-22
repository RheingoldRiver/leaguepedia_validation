from mwparserfromhell import parse
from rivercogutils import login
from leaguepedia_validation.validator import Validator

def test_pick_ban():
	wikitext = parse("""{{PicksAndBansS7|blueteam=CJ Entus |redteam=APK Prince |team1score=1 |team2score=0 |winner=1
	|blueban1=malzahar      |red_ban1=leblanc
	|blueban2=jayce      |red_ban2=kha'zix
	|blueban3=varus      |red_ban3=rengar
	|bluepick1=camille     |bluerole1=top
	                                           |red_pick1=elise    |red_role1=jungle
	                                           |red_pick2=syndra    |red_role2=mid
	|bluepick2=corki     |bluerole2=mid
	|bluepick3=jhin     |bluerole3=ad
	                                           |red_pick3=shen    |red_role3=top
	|blueban4=ashe      |red_ban4=zyra
	|blueban5=caitlyn      |red_ban5=thresh
	                                           |red_pick4=karma    |red_role4=support
	|bluepick4=rek'sai     |bluerole4=jg
	|bluepick5=tahm kench     |bluerole5=support
	                                           |red_pick5=ezreal    |red_role5=ad
	|game1=Yes}}""")
	
	validator = Validator(site=login('me', 'lol'))
	for template in wikitext.filter_templates():
		print('Should be no error:')
		perform_one_test(validator, template)
		
		# create a role error
		template.add('bluerole4', 's')
		print('Should be RoleError:')
		perform_one_test(validator, template)
		
		# create a champion error
		template.add('bluerole4', 'support')
		template.add('bluepick5', 'rek')
		print('Should be ChampionError:')
		perform_one_test(validator, template)
	
def perform_one_test(validator, template):
	response = validator.validate(template)
	if response.has_errors:
		print(response.errors[0].code)

if __name__ == '__main__':
	test_pick_ban()
