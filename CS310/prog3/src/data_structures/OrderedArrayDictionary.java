package data_structures;

import java.util.ConcurrentModificationException;
import java.util.Iterator;

/**
 * William Fox cssc0917
 * prog3 OrderedArrayDictionary.java
 * Array is ordered with lowest key in array[0]
 */
public class OrderedArrayDictionary<K extends Comparable<K>, V> implements DictionaryADT<K, V> {

    private int capactiy, currentSize;
    private long modificationCounter;
    private DictionaryElement<K, V>[] array;

    public OrderedArrayDictionary(int size) {
        capactiy = size;
        modificationCounter = currentSize = 0;
        array = new DictionaryElement[capactiy];
    }


    /**
     * Adds the given key/value pair to the dictionary.  Returns
     * false if the dictionary is full, or if the key is a duplicate.
     * Returns true if addition succeeded.
     *
     * @param key
     * @param value
     */
    public boolean add(K key, V value) {
        DictionaryElement<K, V> temp = new DictionaryElement<>(key, value);
        int index = binSearchInsert(temp, 0, currentSize - 1);
        if (index == -1 || isFull())//Keys must be unique
            return false;
        for (int i = currentSize; i > index; i--)
            array[i] = array[i - 1];
        array[index] = temp;
        currentSize++;
        modificationCounter++;
        return true;
    }

    /**
     * Deletes the key/value pair identified by the key parameter.
     * Returns true if the key/value pair was found and removed, otherwise false.
     *
     * @param key
     */
    public boolean delete(K key) {
        if (isEmpty()) return false;
        int index = binSearch(new DictionaryElement<K, V>(key, null), 0, currentSize - 1);
        if (index == -1)
            return false;
        for (int i = index; i < currentSize - 1; i++)
            array[i] = array[i + 1];
        currentSize--;
        modificationCounter++;
        return true;
    }

    /**
     * Returns true if the dictionary has an object identified by
     * key in it, otherwise false.
     *
     * @param key
     */
    public boolean contains(K key) {
        return getValue(key) != null;
    }

    /**
     * Returns the value associated with the parameter key.  Returns
     * null if the key is not found or the dictionary is empty.
     *
     * @param key
     */
    public V getValue(K key) {
        if (isEmpty()) return null;
        int index = binSearch(new DictionaryElement<K, V>(key, null), 0, currentSize - 1);
        if (index == -1) //Not Found
            return null;
        return array[index].value;
    }

    /**
     * Returns the key associated with the parameter value.  Returns
     * null if the value is not found in the dictionary.  If more
     * than one key exists that matches the given value, returns the
     * first one found.
     *
     * @param value
     */
    public K getKey(V value) {
        for (int i = 0; i < currentSize; i++)
            if ((((Comparable<V>) array[i].value).compareTo(value) == 0))
                return array[i].key;
        return null;
    }

    /**
     * Returns the number of key/value pairs currently stored
     * in the dictionary
     */
    public int size() {
        return currentSize;
    }

    /**
     * Returns true if the dictionary is at max capacity
     */
    public boolean isFull() {
        return currentSize == capactiy;
    }

    /**
     * Returns true if the dictionary is empty
     */
    public boolean isEmpty() {
        return currentSize == 0;
    }

    /**
     * Returns the Dictionary object to an empty state.
     */
    public void clear() {
        modificationCounter = currentSize = 0;
    }

    //Return Index obj is at or -1 if not found
    private int binSearch(DictionaryElement<K, V> de, int lo, int hi) {
        if (hi < lo) return -1;
        int mid = (lo + hi) / 2;
        int comp = de.compareTo(array[mid]);
        if (comp == 0) return mid;                          //Found
        else if (comp < 0) return binSearch(de, lo, --mid); //Go Left
        return binSearch(de, ++mid, hi);                    //Go Right
    }

    //Returns Index to insert at
    private int binSearchInsert(DictionaryElement<K, V> de, int lo, int hi) {
        if (hi < lo) return lo;
        int mid = (lo + hi) / 2;
        int comp = de.compareTo(array[mid]);
        if (comp == 0) return -1; //Keys must be unique
        else if (comp < 0) return binSearchInsert(de, lo, --mid); //Go Left
        return binSearchInsert(de, ++mid, hi);                    //Go Right
    }


    //~~~~~~~~~~~~~~~~~~~~~Iterators and DictionaryNode Classes Below~~~~~~~~~~~~~~~~~~~~~~~~
    abstract class IteratorHelper<E> implements Iterator<E> {
        protected int index;
        protected long modificationCheck;

        public IteratorHelper() {
            index = 0;
            modificationCheck = modificationCounter;
        }

        public boolean hasNext() {
            if (modificationCheck != modificationCounter)
                throw new ConcurrentModificationException();
            return index < currentSize;
        }

        public abstract E next();

        public void remove() {
            throw new UnsupportedOperationException();
        }

    }//IteratorHelper

    private class KeyIteratorHelper extends IteratorHelper<K> {

        public K next() {
            return array[index++].key;
        }
    }

    private class ValueIteratorHelper extends IteratorHelper<V> {

        public V next() {
            return array[index++].value;
        }
    }

    /**
     * Returns an Iterator of the keys in the dictionary, in ascending
     * sorted order.  The iterator must be fail-fast.
     */
    public Iterator<K> keys() {
        return new KeyIteratorHelper();
    }

    /**
     * Returns an Iterator of the values in the dictionary.  The
     * order of the values must match the order of the keys.
     * The iterator must be fail-fast.
     */
    public Iterator<V> values() {
        return new ValueIteratorHelper();
    }


    private class DictionaryElement<K extends Comparable<K>, V> implements Comparable<DictionaryElement<K, V>> {
        K key;
        V value;

        public DictionaryElement(K k, V v) {
            key = k;
            value = v;
        }

        public int compareTo(DictionaryElement<K, V> de) {
            return key.compareTo(de.key);
        }
    }//DictionaryElement

}//Eof
