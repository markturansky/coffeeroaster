class CreateRoasts < ActiveRecord::Migration[5.1]
  def change
    create_table :roasts do |t|
      t.string :name

      t.timestamps
    end
  end
end
