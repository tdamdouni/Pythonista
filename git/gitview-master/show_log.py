import time, textwrap,ui
import dulwich.objects

class log_table(ui.View):
    def __init__(self,r):
        self.r=r
        #takes gitview repo object r
        self.o=r._repo().object_store
        shas=[sha for sha in self.o if isinstance(self.o[sha] , dulwich.objects.Commit)]

        self.shas=sorted(shas,key=lambda x:self.o[x].commit_time , reverse=True)
        #self.commits=[(x,time.ctime(o[x].commit_time),o[x].author,os[x].message) for x in shas]

    def tableview_number_of_sections(self, tableview):
        # untracked, mod unstg, staged, tracked
        return len(self.shas)

    def tableview_number_of_rows(self, tableview, section):
        return 1

        
    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell('value2')
        #cell.height=tableview.row_height
        #cell.width=tableview.width
        sha=self.shas[section]
        commit=self.o[sha]
        commit_time=time.ctime(commit.commit_time)
        message=commit.message
        author=commit.author
        cell.text_label.text='author:\n{}'.format(author)
        cell.text_label.number_of_lines=0
        cell.detail_text_label.text=message
        cell.detail_text_label.number_of_lines=0
        return cell
    def tableview_title_for_header(self, tableview, section):
        sha=self.shas[section]
        commit=self.o[sha]
        commit_time=time.ctime(commit.commit_time)
        message=commit.message
        author=commit.author
        return'{}  <{}>'.format(commit_time, sha[0:7])
    
    def tableview_title_for_delete_button(self, tableview, section, row):
        return 'open'
    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return True

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        tableview.set_editing(False )
        self.r.view['branch'].text=self.shas[section]
        self.r.branch_did_change(self.r)
        tableview.close()
        #pass

def main(r):

    L=log_table(r)
    t=ui.TableView()
    t.row_height=75
    t.data_source=L
    t.delegate=L
    t.frame=(44.0, 44.0, 540.0, 576.0)
    t.present('sheet')

