class Task:
  def __init__(self, id, status, description, title, duedate):
    self.id = id
    self.title = title
    self.description = description
    self.deudate = duedate
    self.status = status

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'duedate':self.duedate,
      'status' :self.status
    }
